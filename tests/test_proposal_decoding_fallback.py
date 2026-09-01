import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class FakeResponse:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self._body = body
        self.headers = {'content-type': 'application/json'}
        self.text = json.dumps(body)

    def json(self):
        return self._body


def load_govbot(temp_dir):
    (temp_dir / 'secrets.json').write_text(json.dumps({
        'IN_PRODUCTION': False,
        'FETCH_LAST_PROP': False,
        'TWITTER': {'ENABLED': False},
        'DISCORD': {'ENABLED': False},
        'EMAIL': {'ENABLED': False},
        'DISCORD_THREADS': {'ENABLE_THREADS_AND_REACTIONS': False},
        'EXPLORER_DEFAULT': 'mintscan',
        'TICKERS_TO_ANNOUNCE': [],
        'TICKERS_TO_IGNORE': [],
        'FILENAME': 'chains.json',
    }))
    (temp_dir / 'chains.json').write_text('{}')

    spec = importlib.util.spec_from_file_location('govbot_under_test', ROOT / 'GovBot.py')
    module = importlib.util.module_from_spec(spec)
    previous_cwd = Path.cwd()
    sys.path.insert(0, str(ROOT))
    os.chdir(temp_dir)
    try:
        spec.loader.exec_module(module)
    finally:
        os.chdir(previous_cwd)
        sys.path.remove(str(ROOT))
    module.EMAIL_FETCHING_ERROR_NOTIFICATION = False
    return module


class ProposalDecodingFallbackTests(unittest.TestCase):
    def test_skips_an_undecodable_proposal_after_a_bulk_wiretype_error(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            module = load_govbot(Path(temporary_directory))
            module.chainAPIs['kiichain_testnet'] = ['https://example.test/cosmos/gov/v1beta1/proposals']
            module.proposals = {'kiichain_testnet': 12}
            module.failure_counter = {'kiichain_testnet': 2}
            module.MAX_CONSECUTIVE_NOT_FOUND = 1

            voting_proposal = {
                'proposal_id': '14',
                'content': {'title': 'A valid proposal', 'description': 'Still reachable'},
                'status': 'PROPOSAL_STATUS_VOTING_PERIOD',
            }

            def fake_get(url, **_kwargs):
                if url.endswith('/proposals'):
                    return FakeResponse(500, {
                        'code': 13,
                        'message': 'proto: wrong wireType = 2 for field Enabled',
                    })
                if url.endswith('/proposals/13'):
                    return FakeResponse(500, {
                        'code': 13,
                        'message': 'collections: encoding error: value decode: proto: wrong wireType = 2 for field Enabled',
                    })
                if url.endswith('/proposals/14'):
                    return FakeResponse(200, {'proposal': voting_proposal})
                return FakeResponse(404, {'code': 5, 'message': 'not found'})

            with patch.object(module.requests, 'get', side_effect=fake_get):
                proposals = module.getAllProposalsWithFallback('kiichain_testnet')

            self.assertEqual(proposals, [voting_proposal])
            self.assertEqual(module.proposals['kiichain_testnet'], 14)
            self.assertEqual(module.failure_counter['kiichain_testnet'], 0)

    def test_preserves_the_existing_generic_decode_skip(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            module = load_govbot(Path(temporary_directory))
            module.chainAPIs['kiichain_testnet'] = ['https://example.test/cosmos/gov/v1beta1/proposals']
            module.proposals = {'kiichain_testnet': 12}
            module.MAX_CONSECUTIVE_NOT_FOUND = 1

            voting_proposal = {
                'proposal_id': '14',
                'content': {'title': 'A valid proposal', 'description': 'Still reachable'},
                'status': 'PROPOSAL_STATUS_VOTING_PERIOD',
            }

            def fake_get(url, **_kwargs):
                if url.endswith('/proposals'):
                    return FakeResponse(500, {'code': 13, 'message': 'runtime error: decoder unavailable'})
                if url.endswith('/proposals/13'):
                    return FakeResponse(200, {'code': 13, 'message': 'failed to decode proposal'})
                if url.endswith('/proposals/14'):
                    return FakeResponse(200, {'proposal': voting_proposal})
                return FakeResponse(404, {'code': 5, 'message': 'not found'})

            with patch.object(module.requests, 'get', side_effect=fake_get):
                proposals = module.getAllProposalsWithFallback('kiichain_testnet')

            self.assertEqual(proposals, [voting_proposal])
            self.assertEqual(module.proposals['kiichain_testnet'], 14)

    def test_does_not_fallback_for_an_unrelated_server_error(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            module = load_govbot(Path(temporary_directory))
            module.chainAPIs['kiichain_testnet'] = ['https://example.test/cosmos/gov/v1beta1/proposals']

            with patch.object(module.requests, 'get', return_value=FakeResponse(500, {
                'code': 13,
                'message': 'upstream service unavailable',
            })) as get:
                proposals = module.getAllProposalsWithFallback('kiichain_testnet')

            self.assertEqual(proposals, [])
            self.assertEqual(get.call_count, 1)


if __name__ == '__main__':
    unittest.main()

