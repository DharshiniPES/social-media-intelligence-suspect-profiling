"""
Technology Detection Module
"""

def detect_technologies(html):

    html = html.lower()

    technologies = []

    signatures = {

        "React": [
            "react",
            "_reactroot",
            "__next"
        ],

        "Vue.js": [
            "vue"
        ],

        "Angular": [
            "ng-app",
            "angular"
        ],

        "Bootstrap": [
            "bootstrap"
        ],

        "Tailwind CSS": [
            "tailwind"
        ],

        "jQuery": [
            "jquery"
        ],

        "WordPress": [
            "wp-content",
            "wp-includes"
        ],

        "Cloudflare": [
            "cloudflare"
        ],

        "Google Analytics": [
            "google-analytics",
            "gtag(",
            "googletagmanager"
        ],

        "Font Awesome": [
            "font-awesome",
            "fontawesome"
        ]

    }

    for tech, patterns in signatures.items():

        if any(

            pattern in html

            for pattern in patterns

        ):

            technologies.append(tech)

    return technologies