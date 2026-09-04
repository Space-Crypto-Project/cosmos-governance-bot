import json
import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from ChainApis import chainAPIs


class ArkeoDelistingTests(unittest.TestCase):
    def test_removes_mainnet_and_preserves_testnet_configuration(self):
        sample_state = json.loads((REPOSITORY_ROOT / 'chains.sample.json').read_text(encoding='utf-8'))

        self.assertNotIn('arkeo', chainAPIs)
        self.assertNotIn('arkeo', sample_state)
        self.assertIn('arkeo_testnet', chainAPIs)
        self.assertIn('arkeo_testnet', sample_state)
        self.assertEqual(
            chainAPIs['arkeo_testnet'][0],
            'https://arkeo-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        )
