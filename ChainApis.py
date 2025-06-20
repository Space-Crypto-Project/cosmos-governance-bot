'''
Dict of chains in the following format:

{
    "ticker": [
        "LCD endpoints for proposals",
        {
            "ping": "https://explorer.spacestake.tech/ticker/gov/",
            "mintscan": "https://mintscan.io/ticker/proposals/",
        },
        "@twitter"
    ]
}

Custom links will only be used if true in the GovBot file
'''

# Define custom explorer links, useful when a chain has its own proposals page
customExplorerLinks = {
    "dig": "https://app.digchain.org/proposals",
    "terra": "https://station.terra.money/proposal",
    # "kuji": "https://kujira.explorers.guru/proposal",
}

JUNO_REST_API = "https://rest-juno.ecostake.com/cosmwasm/wasm/v1/contract/"
DAOs = { # Juno DAO_DAO Chains here
    "raw": {
        "name": "RAW DAO",
        "proposals": f"{JUNO_REST_API}/juno1eqfqxc2ff6ywf8t278ls3h3rdk7urmawyrthagl6dyac29r7c5vqtu0zlf/smart/eyJsaXN0X3Byb3Bvc2FscyI6e319?encoding=base64",
        "vote": "https://www.rawdao.zone/vote",
        "twitter": "@raw_dao",
    }
}

# Defined all info needed for given tickers. If only 1 explorer is found, that one will be used
# no matter what explorer is defined in GovBot
chainAPIs = {
    'juno': [
        'https://juno-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/juno/gov',
            "keplr": 'https://wallet.keplr.app/chains/juno/proposals'
        },
        "@JunoNetwork"
        ],
    'huahua': [
        'https://api.chihuahua.wtf/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/chihuahua/gov',
            "mintscan": 'https://www.mintscan.io/chihuahua/proposals',
        },
        "@ChihuahuaChain"
        ],
    'osmo': [
        'https://lcd-osmosis.blockapsis.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/osmosis/gov',
            "mintscan": 'https://www.mintscan.io/osmosis/proposals',
            "keplr": 'https://wallet.keplr.app/chains/osmosis/proposals'
        },
        '@osmosiszone'
        ],
    'cosmos': [
        'https://cosmos-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/cosmos/gov',
            "mintscan": 'https://www.mintscan.io/cosmos/proposals',
            "keplr": 'https://wallet.keplr.app/chains/cosmos-hub/proposals'
        },
        "@cosmos"
        ],
    'akt': [
        'https://akash-api.polkachu.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/akash-network/gov',
            "mintscan": 'https://www.mintscan.io/akash/proposals',
            "keplr": 'https://wallet.keplr.app/chains/akash/proposals'
        },
        '@akashnet_'
        ],
    'stargaze': [
        "https://stargaze-api.spacestake.tech/cosmos/gov/v1/proposals",
        {
            "ping": 'https://explorer.spacestake.tech/stargaze/gov',
            "mintscan": 'https://www.mintscan.io/stargaze/proposals',
            "keplr": 'https://wallet.keplr.app/chains/stargaze/proposals'
        },        
        '@StargazeZone'
        ],
    'kava': [
        'https://api.data.kava.io/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/kava/gov',
            "mintscan": 'https://www.mintscan.io/kava/proposals',
            "keplr": 'https://wallet.keplr.app/chains/kava/proposals'
        },        
        '@KAVA_CHAIN'
        ],
    'like': [
        'https://mainnet-node.like.co/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/likecoin/gov',
        },        
        '@likecoin'
        ],
    'xprt': [
        'https://rest.core.persistence.one/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/persistence/gov',
            "mintscan": 'https://www.mintscan.io/persistence/proposals',
            "keplr": 'https://wallet.keplr.app/chains/persistence/proposals',
        },        
        '@PersistenceOne'
        ],
    'cmdx': [
        'https://rest.comdex.one/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/comdex/gov',
            "mintscan": 'https://www.mintscan.io/comdex/proposals',
        },        
        '@ComdexOfficial'
        ],
    "bcna": [ 
        'https://lcd.bitcanna.io/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/bitcanna/gov',
            "mintscan": 'https://www.mintscan.io/bitcanna/proposals',
        },        
        '@BitCannaGlobal'
        ],
    "btsg": [ 
        'https://lcd.explorebitsong.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/bitsong/gov',
            "mintscan": 'https://www.mintscan.io/bitsong/proposals',
        },        
        '@BitSongOfficial'
        ],
    "band": [
        'https://laozi1.bandchain.org/api/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/band-protocol/gov',
            "mintscan": 'https://www.mintscan.io/akash/proposals',
        },        
        '@BandProtocol'
        ],
    "boot": [ # Bostrom
        'https://lcd.bostrom.cybernode.ai/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/bostrom/gov',
            "keplr": 'https://wallet.keplr.app/chains/bostrom/proposals',
        },        
        ''
        ],
    "cheqd": [ 
        'https://api.cheqd.net/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/cheqd/gov',
        },        
        '@cheqd_io'
        ],
    "cro": [  
        'https://cronos-rest.publicnode.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/crypto-com-chain/gov',
            "mintscan": 'https://www.mintscan.io/crypto-org/proposals',
            "keplr": 'https://wallet.keplr.app/chains/crypto-org/proposals'
        },        
        '@cryptocom'
        ],
    "evmos": [  
        'https://evmos-api.polkachu.com/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/evmos/gov',
            "mintscan": 'https://www.mintscan.io/evmos/proposals',
            "keplr": 'https://wallet.keplr.app/chains/evmos/proposals/'
        },        
        '@EvmosOrg'
        ],
    "fetch": [
        'https://rest-fetchhub.fetch.ai/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/fetchhub/gov',
            "mintscan": 'https://www.mintscan.io/fetchai/proposals',
        },        
        '@Fetch_ai'
        ],
    "grav": [  
        'https://gravitychain.io:1317/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/gravity-bridge/gov',
            "mintscan": 'https://www.mintscan.io/gravity-bridge/proposals',
            "keplr": 'https://wallet.keplr.app/chains/gravity-bridge/proposals'
        },        
        '@gravity_bridge'
        ],
    "inj": [  
        'https://public.lcd.injective.network/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/injective/gov',
            "mintscan": 'https://www.mintscan.io/injective/proposals',
        },        
        '@InjectiveLabs'
        ],
    "iris": [  
        'https://iris-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/iris-network/gov',
            "mintscan": 'https://www.mintscan.io/iris/proposals',
            "keplr": 'https://wallet.keplr.app/chains/irisnet/proposals'
        },        
        '@irisnetwork'
        ],
    "lum": [  
        'https://node0.mainnet.lum.network/rest/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/lum-network/gov',
            "mintscan": 'https://www.mintscan.io/lum/proposals',
        },        
        '@lum_network'
        ],
    "regen": [  
        'https://regen.stakesystems.io/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/regen/gov',
            "mintscan": 'https://www.mintscan.io/regen/proposals',
            "keplr": 'https://wallet.keplr.app/chains/regen/proposals'
        },        
        '@regen_network'
        ],
    "hash": [  
        'https://api.provenance.io/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/provenance/gov',
        },        
        '@provenancefdn'
        ],
    "secret": [  
        'https://lcd-secret.keplr.app/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/secret/gov',
            "mintscan": 'https://www.mintscan.io/secret/proposals',
            "keplr": 'https://wallet.keplr.app/chains/secret-network/proposals'
        },        
        '@SecretNetwork'
        ],
    "sent": [  
        'https://lcd-sentinel.keplr.app/cosmos/gov/v1beta1/proposals',        
        {
            "ping": 'https://explorer.spacestake.tech/sentinel/gov',
            "mintscan": 'https://www.mintscan.io/sentinel/proposals',
            "keplr": 'https://wallet.keplr.app/chains/sentinel/proposals',
        },        
        '@Sentinel_co'
        ],
    "sif": [  
        'https://sifchain-api.polkachu.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/sifchain/gov',
            "mintscan": 'https://www.mintscan.io/sifchain/proposals',
            "keplr": 'https://wallet.keplr.app/chains/sifchain/proposals'
        },        
        "@sifchain"
        ],
    "kuji": [  
        'https://kujira-api.polkachu.com/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.chaintools.tech/kujira/gov',
        },        
        "@TeamKujira"
        ],        
    "terraC": [  
        'https://blockdaemon-terra-lcd.api.bdnodes.net:1317/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/terra-luna/gov',
        },        
        "@terraC_money"
        ],
    "terra": [  
        'https://phoenix-lcd.terra.dev/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/terra2/gov',
        },        
        "@terra_money"
        ],
    "umee": [  
        'https://umee.api.kjnodes.com/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/umee/gov',
            "mintscan": 'https://www.mintscan.io/umee/proposals',
            "keplr": 'https://wallet.keplr.app/chains/umee/proposals',
        },        
        "@Umee_CrossChain"
        ],
    "kyve": [  
        'https://kyve-api.polkachu.com/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/kyve/gov',
            "keplr": 'https://wallet.keplr.app/chains/kyve/proposals',
        },        
        "@KYVENetwork"
    ],
    "tia": [
        'https://api.lunaroasis.net/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/celestia/gov',
            "mintscan": 'https://www.mintscan.io/celestia/proposals',
            "keplr": 'https://wallet.keplr.app/chains/celestia/proposals',
        },
        "@CelestiaOrg"
    ],
    "axl": [
        'https://axelar-api.polkachu.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/axelar/gov',
            "mintscan": 'https://www.mintscan.io/axelar/proposals',
            "keplr": 'https://wallet.keplr.app/chains/axelar/proposals',
        },
        "@AxelarNetwork"
    ],
    "dydx": [
        'https://dydx-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/dydx/gov',
            "mintscan": 'https://www.mintscan.io/dydx/proposals',
            "keplr": 'https://wallet.keplr.app/chains/dydx/proposals',
        },
        "@dYdX"
    ],
    "stake" : [
        'https://noble-api.polkachu.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/noble/gov',
        },
        ""
    ],
    "zetachain": [
        'https://zetachain.blockpi.network/lcd/v1/public/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/zetachain/gov',
            "mintscan": 'https://www.mintscan.io/zeta/proposals',
        },
        "@zetablockchain"
    ],
    "warden_testnet": [
        'https://warden-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/warden-testnet/gov',

        },
        "@wardenprotocol"
    ],
    "pryzm_testnet": [
        'https://pryzm-testnet-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/pryzm-testnet/gov',

        },
        "@Pryzm_Zone"
    ],
    "lava_testnet": [
        'https://lava-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/lava-testnet/gov',

        },
        "@lavanetxyz"
    ],
    "artela_testnet": [
        'https://artela-testnet-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/artela-testnet/gov',

        },
        "@artela_network"
    ],
    "arkeo_testnet": [
        'https://arkeo-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/arkeo-testnet/gov',

        },
        "@arkeonetwork"
    ],
    "side_testnet": [
        'https://side-testnet-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/side-testnet/gov',

        },
        "@SideProtocol"
    ],
    "elys_testnet": [
        'https://elys-testnet-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/elys-testnet/gov',

        },
        "@elys_network"
    ],
    "elys": [
        'https://elys-api.polkachu.com/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/elys/gov',
        },
        "@elys_network"
    ],
    "galactica_testnet": [
        'https://galactica-testnet-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/galactica-testnet/gov',

        },
        "@GalacticaNet"
    ],
    "Og_testnet": [
        'https://og-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/og-testnet/gov',

        },
        "@0G_labs"
    ]
    ,
    "kopi": [
        'https://kopi-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/kopi/gov',
        },
        "@kopi_money"
    ],
    "kopi_testnet": [
        'https://kopi-testnet-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/kopi-testnet/gov',

        },
        "@kopi_money"
    ],
    "initia_testnet": [
        'https://initia-testnet-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/initia-testnet/gov',

        },
        "@initiaFDN"
    ],
    "initia": [
        'https://initia-api.polkachu.com/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/initia/gov',

        },
        "@initiaFDN"
    ],
    "airchains_testnet": [
        'https://airchains-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/airchains-testnet/gov',

        },
        "@airchains_io"
    ],
    "blockx": [
        'https://blockx-mainnet-api.itrocket.net/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/blockx/gov',

        },
        "@BlockXnet"
    ],
    "fiamma_testnet": [
        'https://fiamma-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/fiamma-testnet/gov',

        },
        "@Fiamma_Chain"
    ],
    "allora_testnet": [
        'https://allora-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/allora-testnet/gov',

        },
        "@AlloraNetwork"
    ],
    "empeiria_testnet": [
        'https://empeiria-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/empeiria-testnet/gov',

        },
        "@empe_io"
    ],
    "prysm_testnet": [
        'https://prysm-testnet-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/prysm-testnet/gov',

        },
        "@PrysmNetwork"
    ],
    "zenrock_testnet": [
        'https://zenrock-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/zenrock-testnet/gov',

        },
        "@OfficialZenrock"
    ],
    "tellor_testnet": [
        'https://tellor-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/tellor-testnet/gov',

        },
        "@wearetellor"
    ],
    "atomone_testnet": [
        'https://atomone-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/atomone-testnet/gov',

        },
        "@_atomone"
    ],
    "kiichain_testnet": [
        'https://kiichain-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/kiichain-testnet/gov',

        },
        "@KiiChainio"
    ],
    "axone_testnet": [
        'https://axone-testnet-api.spacestake.tech/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/axone-testnet/gov',

        },
        "@axonexyz"
    ],
    "arkeo": [
        'https://arkeo-api.spacestake.tech/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/arkeo/gov',
        },
        "@arkeonetwork"
    ],
}