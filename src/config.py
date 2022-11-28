
VENDOR_DATABASE_CONFIG = {
            'table_name': 'VendorTracking',
            'tracktable_schema':
            {
                "id": str,
                "duration": int
            },
            'db_file': './vendor.db'
}

PLATFORM_TARGET_RATIOS = {
    'YOUTUBE': float(.30),
    'SPOTIFY': float(.10),
    'INSTAGRAM': float(.60),
}
