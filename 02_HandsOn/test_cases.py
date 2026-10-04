test_cases = [
    {
        "input": "iPhone 17 with A19 chip and 6.3-inch display",
        "expected": "Smartphone"
    },
    {
        "input": "MacBook Air with M4 chip and 16GB RAM",
        "expected": "Laptop"
    },
    {
        "input": "iPad Air 11-inch with M3 chip",
        "expected": "Tablet"
    },
    {
        "input": "AirPods Pro with active noise cancellation",
        "expected": "Accessory"
    },
    {
        "input": "Samsung Galaxy S25 Ultra 5G smartphone",
        "expected": "Smartphone"
    },
    {
        "input": "Dell XPS 13 laptop with Intel processor",
        "expected": "Laptop"
    },
    {
        "input": "Samsung Galaxy Tab S10 tablet",
        "expected": "Tablet"
    },
    {
        "input": "Apple Magic Mouse wireless mouse",
        "expected": "Accessory"
    },

    # More challenging examples
    {
        "input": "A portable computer designed for work and travel with a 14-inch screen",
        "expected": "Laptop"
    },
    {
        "input": "A touchscreen device larger than a phone designed for reading and streaming",
        "expected": "Tablet"
    },
    {
        "input": "Wireless earbuds with a charging case and Bluetooth connectivity",
        "expected": "Accessory"
    },
    {
        "input": "A handheld mobile device with cellular connectivity and a rear camera",
        "expected": "Smartphone"
    },
]