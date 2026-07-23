# -*- coding: utf-8 -*-
"""Inline SVG diagrams for the Locumfy docs.
Hand-authored, dependency-free. Palette matches assets/css/docs.css tokens.
To edit a diagram, change the coordinates/labels below and re-run build.py."""

C = {
    "brand": "#1f6feb", "brandd": "#1450b4", "brand050": "#eaf2ff",
    "accent": "#0fb5a6", "accentd": "#0a897d", "accent050": "#e6faf7",
    "ink": "#1b2330", "muted": "#66707e", "line": "#cfd8e3",
    "purple": "#5a3fd0", "purple050": "#f0ecff",
    "amber": "#b5730f", "amber050": "#fff4dc",
    "red": "#c0392b", "red050": "#fdecea", "green": "#1a7f43", "green050": "#e8f8ee",
    "slate050": "#eef2f7",
}

_DEFS = f"""
  <defs>
    <marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L7,3 L0,6 Z" fill="{C['muted']}"/>
    </marker>
    <marker id="arrowb" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L7,3 L0,6 Z" fill="{C['brand']}"/>
    </marker>
  </defs>
"""


def _box(x, y, w, h, label, fill="#fff", stroke=None, tcol=None, sub=None, rx=9, fs=13, bold=True):
    stroke = stroke or C["line"]
    tcol = tcol or C["ink"]
    weight = "700" if bold else "500"
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>']
    if sub:
        out.append(f'<text x="{x+w/2}" y="{y+h/2-4}" text-anchor="middle" font-family="sans-serif" '
                   f'font-size="{fs}" font-weight="{weight}" fill="{tcol}">{label}</text>')
        out.append(f'<text x="{x+w/2}" y="{y+h/2+13}" text-anchor="middle" font-family="sans-serif" '
                   f'font-size="10.5" fill="{C["muted"]}">{sub}</text>')
    else:
        out.append(f'<text x="{x+w/2}" y="{y+h/2+1}" text-anchor="middle" dominant-baseline="middle" '
                   f'font-family="sans-serif" font-size="{fs}" font-weight="{weight}" fill="{tcol}">{label}</text>')
    return "\n".join(out)


def _t(x, y, s, fs=11, col=None, anchor="middle", weight="600"):
    col = col or C["muted"]
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="sans-serif" '
            f'font-size="{fs}" font-weight="{weight}" fill="{col}">{s}</text>')


def _line(x1, y1, x2, y2, col=None, marker="arrow", dash=None, w=1.5):
    col = col or C["muted"]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{d}{m}/>'


def _wrap(vb_w, vb_h, inner):
    return (f'<svg viewBox="0 0 {vb_w} {vb_h}" role="img" xmlns="http://www.w3.org/2000/svg">'
            f'{_DEFS}{inner}</svg>')


# --------------------------------------------------------------------------
# 1. System context (Overview)
# --------------------------------------------------------------------------
def system_context():
    s = []
    # actors
    s.append(_t(120, 30, "USERS", 11, C["muted"]))
    s.append(_box(40, 45, 160, 40, "Medical Professional", C["brand050"], C["brand"], C["brandd"], sub="candidate role"))
    s.append(_box(40, 100, 160, 40, "Facility / Employer", C["brand050"], C["brand"], C["brandd"], sub="facility role"))
    s.append(_box(40, 155, 160, 40, "Internal Staff", C["purple050"], C["purple"], C["purple"], sub="admin / investor"))
    # clients
    s.append(_t(370, 30, "CLIENT APPS", 11, C["muted"]))
    s.append(_box(300, 45, 150, 40, "Mobile App", "#fff", C["line"], C["ink"], sub="Flutter / Dart"))
    s.append(_box(300, 100, 150, 40, "Website", "#fff", C["line"], C["ink"], sub="React + Vite"))
    s.append(_box(300, 155, 150, 40, "Admin Site", "#fff", C["line"], C["ink"], sub="React + Vite"))
    # apis
    s.append(_t(620, 30, "REST APIs", 11, C["muted"]))
    s.append(_box(550, 65, 150, 55, "WebsiteApi", C["accent050"], C["accent"], C["accentd"], sub="ASP.NET Core /v1"))
    s.append(_box(550, 150, 150, 45, "AdminWebsiteApi", C["accent050"], C["accent"], C["accentd"], sub="analytics /v1"))
    # core
    s.append(_box(550, 225, 150, 40, "Service Layer", "#fff", C["line"], C["ink"], sub="Services.Core"))
    s.append(_box(550, 285, 150, 40, "EF Core DataContext", "#fff", C["line"], C["ink"], sub="~120 entities"))
    s.append(_box(560, 345, 130, 34, "Relational database", C["slate050"], C["line"], C["ink"], fs=10.5))
    # externals
    s.append(_t(830, 30, "EXTERNAL", 11, C["muted"]))
    s.append(_box(770, 45, 190, 34, "AWS S3 / KMS / SQS", C["amber050"], C["amber"], C["amber"], fs=11))
    s.append(_box(770, 88, 190, 34, "Cloud / Local LLM", C["amber050"], C["amber"], C["amber"], fs=11))
    s.append(_box(770, 131, 190, 34, "OCR Web Service", C["amber050"], C["amber"], C["amber"], fs=11))
    s.append(_box(770, 174, 190, 34, "NPI Registry / Geolocation", C["amber050"], C["amber"], C["amber"], fs=11))
    # edges actors->clients
    s.append(_line(200, 65, 298, 65, marker="arrowb", col=C["brand"]))
    s.append(_line(200, 120, 298, 120, marker="arrowb", col=C["brand"]))
    s.append(_line(200, 175, 298, 175, marker="arrowb", col=C["purple"]))
    # clients->apis
    s.append(_line(450, 65, 548, 88, marker="arrow"))
    s.append(_line(450, 120, 548, 95, marker="arrow"))
    s.append(_line(450, 175, 548, 172, marker="arrow"))
    # apis->core
    s.append(_line(625, 120, 625, 223, marker="arrow"))
    s.append(_line(625, 195, 625, 223, marker="arrow"))
    s.append(_line(625, 265, 625, 283, marker="arrow"))
    s.append(_line(625, 325, 625, 343, marker="arrow"))
    # core->externals
    s.append(_line(700, 250, 768, 100, marker="arrow", dash="4 3"))
    s.append(_line(700, 250, 768, 150, marker="arrow", dash="4 3"))
    s.append(_line(700, 250, 768, 62, marker="arrow", dash="4 3"))
    s.append(_line(700, 260, 768, 190, marker="arrow", dash="4 3"))
    return _wrap(975, 395, "\n".join(s))


# --------------------------------------------------------------------------
# 2. Layered architecture
# --------------------------------------------------------------------------
def layers():
    # Each band reserves a ~30px title row at the top; boxes are placed BELOW it
    # so the band label never overlaps the content boxes.
    s = []
    X, W = 150, 620
    def band(y, h, title):
        s.append(_box(X, y, W, h, "", "#fff", C["line"], rx=10))
        s.append(_t(X + 15, y + 22, title, 12, C["ink"], anchor="start", weight="800"))
    # Presentation  (band 20–116, title row ~42, boxes 54–102)
    band(20, 96, "PRESENTATION")
    s.append(_box(170, 54, 175, 48, "Mobile App", C["brand050"], C["brand"], C["brandd"], sub="Flutter"))
    s.append(_box(360, 54, 175, 48, "Website", C["brand050"], C["brand"], C["brandd"], sub="React SPA"))
    s.append(_box(550, 54, 200, 48, "Admin Site", C["purple050"], C["purple"], C["purple"], sub="React SPA"))
    # API  (band 132–222, boxes 166–210)
    band(132, 90, "API  (ASP.NET Core, JWT, Swagger)")
    s.append(_box(170, 166, 260, 44, "WebsiteApi", C["accent050"], C["accent"], C["accentd"], sub="candidate + employer"))
    s.append(_box(445, 166, 305, 44, "AdminWebsiteApi", C["accent050"], C["accent"], C["accentd"], sub="analytics dashboards"))
    # Service  (band 238–348, boxes 274–330)
    band(238, 110, "SERVICE  (feature-sliced, Scrutor DI, validation)")
    s.append(_box(170, 274, 175, 56, "Services.Core", "#fff", C["line"], C["ink"], sub="12 feature slices"))
    s.append(_box(357, 274, 130, 56, "Services.AdminCore", "#fff", C["line"], C["ink"], sub="analytics", fs=11.5))
    s.append(_box(499, 274, 110, 56, "ResumeBuilder", "#fff", C["line"], C["ink"], sub="PDF gen", fs=12))
    s.append(_box(621, 274, 129, 56, "AiData + Parsing", "#fff", C["line"], C["ink"], sub="prompts / extract", fs=11.5))
    # Data  (band 364–438, box 400–424)
    band(364, 74, "DATA  (Entity Framework Core 10, code-first)")
    s.append(_box(170, 400, 580, 24, "DataStorage — DataContext + ~120 entities + IEntityTypeConfiguration", C["slate050"], C["line"], C["ink"], rx=6, fs=11.5))
    # Cross-cutting rail (left)
    s.append(_box(20, 20, 115, 418, "", C["accent050"], C["accent"], rx=10))
    s.append(_t(77, 42, "CROSS-", 11, C["accentd"], weight="800"))
    s.append(_t(77, 56, "CUTTING", 11, C["accentd"], weight="800"))
    for i, (lab, sub) in enumerate([("Infrastructure", "validation"), ("AwsCore", "S3/KMS/SQS"),
                                     ("Nullref.Common.*", "shared libs"), ("EFCore.Extensions", "context base")]):
        yy = 78 + i * 82
        s.append(_box(30, yy, 95, 60, lab, "#fff", C["accent"], C["accentd"], sub=sub, fs=10.5, rx=8))
    # flow arrows down between bands
    for y1, y2 in ((116, 130), (222, 236), (348, 362)):
        s.append(_line(460, y1, 460, y2, marker="arrow"))
    return _wrap(770, 452, "\n".join(s))


# --------------------------------------------------------------------------
# 3. Project dependency graph
# --------------------------------------------------------------------------
def dependency_graph():
    s = []
    nodes = {
        "WebsiteApi":      (330, 20, 150, 40, C["accent050"], C["accentd"]),
        "AdminWebsiteApi": (620, 20, 160, 40, C["accent050"], C["accentd"]),
        "Services.Core":   (330, 100, 150, 40, C["brand050"], C["brandd"]),
        "Services.AdminCore": (620, 100, 160, 40, C["brand050"], C["brandd"]),
        "AiData":          (40, 180, 120, 38, "#fff", C["ink"]),
        "ResumeBuilder":   (180, 180, 140, 38, "#fff", C["ink"]),
        "ResumeParser":    (340, 180, 130, 38, "#fff", C["ink"]),
        "Parsing":         (490, 180, 110, 38, "#fff", C["ink"]),
        "Infrastructure":  (620, 180, 160, 38, C["accent050"], C["accentd"]),
        "Parsing.PdfUtils":(490, 250, 130, 38, "#fff", C["ink"]),
        "AwsCore":         (620, 250, 160, 38, C["accent050"], C["accentd"]),
        "DataStorage":     (300, 320, 220, 40, C["slate050"], C["ink"]),
    }
    for name, (x, y, w, h, fill, tc) in nodes.items():
        s.append(_box(x, y, w, h, name, fill, C["line"], tc, fs=12))
    def ctr(n):
        x, y, w, h, *_ = nodes[n]
        return (x + w/2, y + h/2, x, y, w, h)
    edges = [
        ("WebsiteApi", "Services.Core"),
        ("AdminWebsiteApi", "Services.AdminCore"),
        ("Services.Core", "AiData"), ("Services.Core", "ResumeBuilder"),
        ("Services.Core", "ResumeParser"), ("Services.Core", "Parsing"),
        ("Services.Core", "Infrastructure"), ("Services.Core", "DataStorage"),
        ("Services.AdminCore", "DataStorage"), ("Services.AdminCore", "Infrastructure"),
        ("ResumeParser", "ResumeBuilder"), ("ResumeParser", "Parsing"),
        ("ResumeBuilder", "DataStorage"), ("Parsing", "Parsing.PdfUtils"),
        ("AiData", "DataStorage"), ("AwsCore", "Infrastructure"),
    ]
    for a, b in edges:
        ax, ay, axx, ayy, aw, ah = ctr(a)
        bx, by, bxx, byy, bw, bh = ctr(b)
        # connect from bottom of a to top of b (approx)
        y1 = ayy + ah
        y2 = byy
        if by < ay:  # b above a
            y1 = ayy; y2 = byy + bh
        s.append(_line(ax, y1, bx, y2, col=C["line"], marker="arrow", w=1.3))
    s.append(_t(400, 378, "arrow = “references / depends on”   ·   AwsCore composed at startup via reflection", 10.5, C["muted"]))
    return _wrap(820, 392, "\n".join(s))


# --------------------------------------------------------------------------
# 4. Job application state machine
# --------------------------------------------------------------------------
def job_state_machine():
    s = []
    s.append(_box(30, 150, 90, 40, "Open Job", C["slate050"], C["line"], C["ink"], fs=12))
    s.append(_box(190, 150, 150, 46, "Provider_Accepted", C["brand050"], C["brand"], C["brandd"], sub="candidate applied"))
    s.append(_box(190, 40, 150, 40, "Provider_Rejected", C["red050"], C["red"], C["red"], sub="candidate cancelled", fs=12))
    s.append(_box(430, 150, 150, 46, "Facility_Accepted", C["green050"], C["green"], C["green"], sub="employer hired"))
    s.append(_box(430, 40, 150, 40, "FacilityRejected", C["red050"], C["red"], C["red"], sub="employer declined", fs=12))
    s.append(_box(660, 150, 130, 46, "Complete", C["purple050"], C["purple"], C["purple"], sub="job closed"))
    # transitions
    s.append(_line(120, 170, 188, 170, marker="arrow"))
    s.append(_t(154, 163, "apply", 10, C["muted"]))
    s.append(_line(265, 150, 265, 82, marker="arrow", col=C["red"]))
    s.append(_t(300, 118, "cancel", 10, C["red"]))
    s.append(_line(340, 168, 428, 168, marker="arrow", col=C["green"]))
    s.append(_t(384, 161, "accept", 10, C["green"]))
    s.append(_line(505, 150, 505, 82, marker="arrow", col=C["red"]))
    s.append(_t(538, 118, "reject", 10, C["red"]))
    s.append(_line(580, 170, 658, 170, marker="arrow", col=C["purple"]))
    s.append(_t(619, 163, "complete", 10, C["purple"]))
    # side-effect note
    s.append(_box(360, 250, 380, 60, "", C["amber050"], C["amber"], rx=8))
    s.append(_t(378, 272, "On Facility_Accepted:", 11, C["amber"], anchor="start", weight="800"))
    s.append(_t(378, 290, "• all other Provider_Accepted apps for that candidate → rejected", 10.5, C["ink"], anchor="start", weight="500"))
    s.append(_t(378, 304, "• candidate is locked to one active job; Job.FilledJobApplicationId stamped", 10.5, C["ink"], anchor="start", weight="500"))
    s.append(_t(150, 300, "Terminal (read-only):", 11, C["muted"], anchor="start", weight="700"))
    s.append(_box(150, 250, 180, 34, "Provider_Rejected / FacilityRejected", "#fff", C["line"], C["ink"], fs=9.5))
    return _wrap(810, 322, "\n".join(s))


# --------------------------------------------------------------------------
# 5. Timesheet lifecycle
# --------------------------------------------------------------------------
def timesheet_lifecycle():
    s = []
    st = [("Open", "1", C["slate050"], C["ink"]),
          ("ProviderApproved", "2", C["brand050"], C["brandd"]),
          ("ClientApproved", "3", C["green050"], C["green"]),
          ("Paid", "5", C["purple050"], C["purple"])]
    x = 30
    xs = []
    for lab, num, fill, tc in st:
        s.append(_box(x, 60, 155, 46, lab, fill, tc, tc, sub=f"state {num}"))
        xs.append(x)
        x += 210
    labels = ["candidate submits", "employer approves", "payment"]
    for i in range(3):
        x1 = xs[i] + 155
        x2 = xs[i+1]
        s.append(_line(x1, 83, x2-2, 83, marker="arrow"))
        s.append(_t((x1+x2)/2, 76, labels[i], 10, C["muted"]))
    # rejected
    s.append(_box(240, 160, 155, 42, "Rejected", C["red050"], C["red"], C["red"], sub="state 4"))
    s.append(_line(300, 106, 300, 158, marker="arrow", col=C["red"]))
    s.append(_t(340, 135, "employer rejects", 10, C["red"], anchor="start"))
    s.append(_t(430, 185, "Only the candidate creates timesheets, and only for a Facility_Accepted job.", 10.5, C["muted"], anchor="start"))
    s.append(_t(430, 200, "Only the posting employer approves them. Rendered to HTML → PDF (Puppeteer).", 10.5, C["muted"], anchor="start"))
    return _wrap(880, 220, "\n".join(s))


# --------------------------------------------------------------------------
# 6. Resume / AI pipeline
# --------------------------------------------------------------------------
def resume_pipeline():
    s = []
    s.append(_box(20, 90, 130, 48, "Raw resume", "#fff", C["line"], C["ink"], sub="PDF/DOC/RTF/TXT"))
    s.append(_box(180, 90, 140, 48, "Text extract", C["brand050"], C["brand"], C["brandd"], sub="PdfPig / DocConv"))
    s.append(_box(180, 170, 140, 40, "OCR fallback", C["amber050"], C["amber"], C["amber"], sub="image PDFs", fs=11.5))
    s.append(_box(350, 90, 150, 48, "Parse engine", C["brand050"], C["brand"], C["brandd"], sub="~19 section parsers"))
    s.append(_box(530, 90, 150, 48, "ResumeStandardItem", "#fff", C["line"], C["ink"], sub="structured graph", fs=11.5))
    s.append(_box(530, 175, 150, 44, "Candidate + *List", C["accent050"], C["accentd"], C["accentd"], sub="EF Core rows", fs=11.5))
    # downstream
    s.append(_box(730, 20, 200, 42, "Standardized / Anonymized PDF", "#fff", C["line"], C["ink"], sub="employer download", fs=10.5))
    s.append(_box(730, 90, 200, 42, "AI career summary", C["purple050"], C["purple"], C["purple"], sub="cloud / local LLM", fs=11))
    s.append(_box(730, 160, 200, 42, "AI verification notes", C["purple050"], C["purple"], C["purple"], sub="pubs / presentations", fs=11))
    s.append(_box(730, 230, 200, 42, "ML training export", C["slate050"], C["line"], C["ink"], sub="txt / json pairs", fs=11))
    s.append(_line(150, 114, 178, 114, marker="arrow"))
    s.append(_line(250, 138, 250, 168, marker="arrow", dash="4 3", col=C["amber"]))
    s.append(_line(320, 114, 348, 114, marker="arrow"))
    s.append(_line(500, 114, 528, 114, marker="arrow"))
    s.append(_line(605, 138, 605, 173, marker="arrow"))
    s.append(_line(680, 197, 728, 50, marker="arrow", dash="4 3"))
    s.append(_line(680, 197, 728, 111, marker="arrow", dash="4 3"))
    s.append(_line(680, 197, 728, 181, marker="arrow", dash="4 3"))
    s.append(_line(680, 197, 728, 251, marker="arrow", dash="4 3"))
    return _wrap(945, 288, "\n".join(s))


# --------------------------------------------------------------------------
# 7. Core data domains (entity clusters)
# --------------------------------------------------------------------------
def data_domains():
    s = []
    # Candidate hub
    s.append(_box(310, 150, 170, 50, "Candidate", C["brand050"], C["brand"], C["brandd"], sub="IUserAccount hub"))
    prof = ["Employment", "Education", "Certification", "StateLicense", "Skill / Language",
            "Award / Research", "Publication", "Reference", "Specialty"]
    import math
    for i, p in enumerate(prof):
        ang = (i / len(prof)) * 2 * math.pi
        cx = 395 + 250 * math.cos(ang)
        cy = 175 + 135 * math.sin(ang)
        s.append(_box(cx-70, cy-16, 140, 32, "Candidate" + p.split(" / ")[0], "#fff", C["line"], C["ink"], fs=10, rx=6))
        s.append(_line(395 + 90*math.cos(ang), 175 + 55*math.sin(ang),
                       cx - 62*math.cos(ang), cy - 15*math.sin(ang), col=C["line"], marker=None, w=1.1))
    # Employer / job cluster
    s.append(_box(770, 60, 150, 40, "Company", C["accent050"], C["accentd"], C["accentd"], sub="tenant"))
    s.append(_box(770, 120, 150, 40, "Employer", C["accent050"], C["accentd"], C["accentd"], sub="IUserAccount"))
    s.append(_box(770, 190, 150, 40, "Job", "#fff", C["line"], C["ink"], sub="posting"))
    s.append(_box(770, 255, 150, 40, "JobApplication", C["amber050"], C["amber"], C["amber"], sub="state machine"))
    s.append(_box(770, 320, 150, 40, "Timesheet", C["purple050"], C["purple"], C["purple"], sub="weekly"))
    s.append(_line(845, 100, 845, 118, marker="arrow", w=1.1))
    s.append(_line(845, 160, 845, 188, marker="arrow", w=1.1))
    s.append(_line(845, 230, 845, 253, marker="arrow", w=1.1))
    s.append(_line(845, 295, 845, 318, marker="arrow", w=1.1))
    # candidate<->application
    s.append(_line(480, 180, 768, 272, marker="arrow", col=C["amber"], dash="4 3", w=1.3))
    s.append(_t(620, 232, "applies to", 10, C["amber"]))
    # engagement cluster
    s.append(_box(40, 30, 150, 34, "MessageThread", C["slate050"], C["line"], C["ink"], fs=11))
    s.append(_box(40, 74, 150, 34, "MemberPost / Feed", C["slate050"], C["line"], C["ink"], fs=11))
    s.append(_box(40, 300, 150, 34, "CandidateNetwork", C["slate050"], C["line"], C["ink"], fs=11))
    s.append(_box(40, 344, 150, 34, "Document (S3)", C["slate050"], C["line"], C["ink"], fs=11))
    return _wrap(940, 400, "\n".join(s))


DIAGRAMS = {
    "system_context": system_context,
    "layers": layers,
    "dependency_graph": dependency_graph,
    "job_state_machine": job_state_machine,
    "timesheet_lifecycle": timesheet_lifecycle,
    "resume_pipeline": resume_pipeline,
    "data_domains": data_domains,
}
