from modules.report_generator import (
    generate_report,
    save_report
)

report = generate_report(

    "289683",

    0.331,

    "Matching behavioral fingerprint",

    "Part of suspicious community"

)

filename = save_report(

    "289683",

    report

)

print(
    "Saved:",
    filename
)