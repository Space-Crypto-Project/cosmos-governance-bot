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
        'https://juno.stakesystems.io/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/juno/gov',
            "mintscan": 'https://www.mintscan.io/juno/proposals',
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
    'atom': [
        'https://lcd-cosmoshub.keplr.app/cosmos/gov/v1beta1/proposals',
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
    'stars': [
        "https://rest.stargaze-apis.com/cosmos/gov/v1beta1/proposals",
        {
            "ping": 'https://explorer.spacestake.tech/stargaze/gov',
            "mintscan": 'https://www.mintscan.io/stargaze/proposals',
            "keplr": 'https://wallet.keplr.app/chains/stargaze/proposals'
        },        
        '@StargazeZone'
        ],
    'kava': [
        'https://api.data.kava.io/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/kava/gov',
            "mintscan": 'https://www.mintscan.io/kava/proposals',
            "keplr": 'https://wallet.keplr.app/chains/kava/proposals'
        },        
        '@kava_platform'
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
        'https://rest.bd.evmos.org:1317/cosmos/gov/v1beta1/proposals',
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
        'https://lcd-iris.keplr.app/cosmos/gov/v1/proposals',
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
            "mintscan": 'https://www.mintscan.io/kyve/proposals',
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
        'https://dydx-dao-api.polkachu.com/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/dydx/gov',
            "mintscan": 'https://www.mintscan.io/dydx/proposals',
            "keplr": 'https://wallet.keplr.app/chains/dydx/proposals',
        },
        ""
    ],
    "stake" : [
        'https://noble-api.polkachu.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/noble/gov',
        },
        ""
    ],
    "zeta": [
        'https://zetachain.blockpi.network/lcd/v1/public/cosmos/gov/v1/proposals',
        {
            "ping": 'https://explorer.spacestake.tech/zetachain/gov',
        
        },
        ""
    ],

}