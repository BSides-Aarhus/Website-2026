#!/usr/bin/env python3
"""Append one speaker slide per content/speakers/*.md to the design template PPTX."""
import os, re, shutil, zipfile
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "Plans" / "template-output" / "bsides-aarhus-2026-template.pptx"
SPEAKERS_DIR = ROOT / "content" / "speakers"
PHOTOS_DIR = ROOT / "static" / "images" / "speakers"
OUT = TEMPLATE  # overwrite in place

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

def parse_speaker(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm_raw, body = m.group(1), m.group(2).strip()
    fm = {}
    links = {}
    in_links = False
    for line in fm_raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("links:"):
            in_links = True
            continue
        if in_links and line.startswith("  "):
            k, _, v = line.strip().partition(":")
            links[k.strip()] = v.strip().strip('"').strip("'")
            continue
        in_links = False
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    fm["links"] = links
    # bio: first paragraph (or join short ones)
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    fm["bio"] = paragraphs[0] if paragraphs else ""
    fm["slug"] = md_path.stem
    return fm

def find_photo(slug: str):
    for ext in ("jpg", "jpeg", "png"):
        p = PHOTOS_DIR / f"{slug}.{ext}"
        if p.exists():
            return p
    return None

def xml_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))

def build_handle_line(links: dict) -> str:
    parts = []
    if "linkedin" in links:
        # extract handle from /in/<handle>/
        m = re.search(r"/in/([^/]+)/?", links["linkedin"])
        if m:
            parts.append(f"linkedin.com/in/{m.group(1)}")
        else:
            parts.append(links["linkedin"])
    if "website" in links:
        site = re.sub(r"^https?://", "", links["website"]).rstrip("/")
        parts.append(site)
    if "twitter" in links:
        m = re.search(r"twitter\.com/([^/]+)", links["twitter"])
        if m:
            parts.append(f"@{m.group(1)}")
        else:
            parts.append(links["twitter"])
    if "mastodon" in links:
        parts.append(links["mastodon"])
    return "  ·  ".join(parts)

def build_slide_xml(speaker, photo_rid):
    """Build a speaker slide XML by adapting slide5 template."""
    name = xml_escape(speaker["title"])
    role = xml_escape(speaker.get("tagline", ""))
    bio = xml_escape(speaker.get("bio", ""))
    handle = xml_escape(build_handle_line(speaker.get("links", {})))

    # Image position inside the rounded rectangle (rect: x=548640 y=1463040 w=3840480 h=4389120)
    # Place a square photo centered horizontally near top of card
    img_size = 3108960
    img_x = 548640 + (3840480 - img_size) // 2  # 914400
    img_y = 1645920  # 182880 below top of card
    photo_xml = (
        f'<p:pic><p:nvPicPr><p:cNvPr id="100" name="SpeakerPhoto"/>'
        f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
        f'<p:blipFill><a:blip r:embed="{photo_rid}"/>'
        f'<a:srcRect/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
        f'<p:spPr><a:xfrm><a:off x="{img_x}" y="{img_y}"/><a:ext cx="{img_size}" cy="{img_size}"/></a:xfrm>'
        f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 4000"/></a:avLst></a:prstGeom></p:spPr></p:pic>'
    )

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr><p:pic><p:nvPicPr><p:cNvPr id="2" name="Picture 1" descr="_bg.png"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12191695" cy="6858000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic><p:pic><p:nvPicPr><p:cNvPr id="3" name="Picture 2" descr="logo.png"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rId3"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="548640" y="457200"/><a:ext cx="617838" cy="457200"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic><p:sp><p:nvSpPr><p:cNvPr id="4" name="Rounded Rectangle 3"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="548640" y="1463040"/><a:ext cx="3840480" cy="4389120"/></a:xfrm><a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 4000"/></a:avLst></a:prstGeom><a:solidFill><a:srgbClr val="1A1A25"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:style><a:lnRef idx="1"><a:schemeClr val="accent1"/></a:lnRef><a:fillRef idx="3"><a:schemeClr val="accent1"/></a:fillRef><a:effectRef idx="2"><a:schemeClr val="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="lt1"/></a:fontRef></p:style><p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"/><a:endParaRPr/></a:p></p:txBody></p:sp>{photo_xml}<p:sp><p:nvSpPr><p:cNvPr id="6" name="Rectangle 5"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="4754880" y="1371600"/><a:ext cx="640080" cy="38100"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="4AB8D2"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:style><a:lnRef idx="1"><a:schemeClr val="accent1"/></a:lnRef><a:fillRef idx="3"><a:schemeClr val="accent1"/></a:fillRef><a:effectRef idx="2"><a:schemeClr val="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="lt1"/></a:fontRef></p:style><p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"/><a:endParaRPr/></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="7" name="TextBox 6"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="4754880" y="1508760"/><a:ext cx="6858000" cy="365760"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/><a:r><a:rPr sz="1400" b="1"><a:solidFill><a:srgbClr val="4AB8D2"/></a:solidFill><a:latin typeface="JetBrains Mono"/></a:rPr><a:t>SPEAKER</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="8" name="TextBox 7"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="4754880" y="1920240"/><a:ext cx="6858000" cy="822960"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/><a:r><a:rPr sz="4000" b="1"><a:solidFill><a:srgbClr val="E8E8ED"/></a:solidFill><a:latin typeface="Inter"/></a:rPr><a:t>{name}</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="9" name="TextBox 8"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="4754880" y="2788920"/><a:ext cx="6858000" cy="457200"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/><a:r><a:rPr sz="2000" b="0"><a:solidFill><a:srgbClr val="6DD0E7"/></a:solidFill><a:latin typeface="Inter"/></a:rPr><a:t>{role}</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="10" name="TextBox 9"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="4754880" y="3474720"/><a:ext cx="6858000" cy="2103120"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"/><a:lstStyle/><a:p><a:pPr algn="l"/><a:r><a:rPr sz="1600" b="0"><a:solidFill><a:srgbClr val="8888A0"/></a:solidFill><a:latin typeface="Inter"/></a:rPr><a:t>{bio}</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="11" name="TextBox 10"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="4754880" y="5669280"/><a:ext cx="6858000" cy="365760"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/><a:r><a:rPr sz="1400" b="0"><a:solidFill><a:srgbClr val="4AB8D2"/></a:solidFill><a:latin typeface="JetBrains Mono"/></a:rPr><a:t>{handle}</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="12" name="TextBox 11"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="548640" y="6446520"/><a:ext cx="7315200" cy="274320"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/><a:r><a:rPr sz="1000" b="0"><a:solidFill><a:srgbClr val="8888A0"/></a:solidFill><a:latin typeface="JetBrains Mono"/></a:rPr><a:t>BSides Aarhus 2026  ·  June 20  ·  INCUBA Next, Aarhus</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="13" name="TextBox 12"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="10515600" y="6446520"/><a:ext cx="1188720" cy="274320"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="r"/><a:r><a:rPr sz="1000" b="0"><a:solidFill><a:srgbClr val="8888A0"/></a:solidFill><a:latin typeface="JetBrains Mono"/></a:rPr><a:t>Speaker</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''


def build_rels_xml(photo_target: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout7.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image2.png"/><Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{photo_target}"/></Relationships>'''


def main():
    speaker_files = sorted(
        p for p in SPEAKERS_DIR.glob("*.md")
        if not p.stem.endswith(".da") and not p.stem.startswith("_")
    )
    speakers = []
    for sf in speaker_files:
        s = parse_speaker(sf)
        if not s:
            print(f"skip: {sf.name} (no frontmatter)")
            continue
        photo = find_photo(s["slug"])
        if not photo:
            print(f"skip: {s['title']} (no photo)")
            continue
        s["photo"] = photo
        speakers.append(s)

    print(f"Building slides for {len(speakers)} speakers")

    # Read template into memory
    with zipfile.ZipFile(TEMPLATE, "r") as zin:
        files = {name: zin.read(name) for name in zin.namelist()}

    # Existing media images: image1.png (bg), image2.png (logo), image3.png (?). Next index = 4.
    existing_media = sorted([n for n in files if n.startswith("ppt/media/")])
    next_idx = len(existing_media) + 1

    # Existing slides count
    existing_slide_count = 5

    # Compute next presentation rId (existing max is rId10 per inspection)
    pres_rels = files["ppt/_rels/presentation.xml.rels"].decode("utf-8")
    max_rid = max(int(m) for m in re.findall(r'Id="rId(\d+)"', pres_rels))

    pres_xml = files["ppt/presentation.xml"].decode("utf-8")
    ct_xml = files["[Content_Types].xml"].decode("utf-8")

    new_slide_rels = []
    new_slide_ids = []
    next_sld_id = 261  # after 260

    for i, sp in enumerate(speakers, start=1):
        slide_num = existing_slide_count + i
        # Image
        ext = sp["photo"].suffix.lower().lstrip(".")
        if ext == "jpeg":
            ext = "jpg"
        img_name = f"image{next_idx}.{ext}"
        next_idx += 1
        photo_bytes = sp["photo"].read_bytes()
        # Pre-crop to square (center crop) so the photo fills the square box cleanly
        try:
            from io import BytesIO
            img = Image.open(BytesIO(photo_bytes))
            img = ImageOps.exif_transpose(img)
            w, h = img.size
            side = min(w, h)
            left = (w - side) // 2
            top = (h - side) // 2
            img = img.crop((left, top, left + side, top + side))
            buf = BytesIO()
            save_fmt = "JPEG" if ext == "jpg" else "PNG"
            if save_fmt == "JPEG" and img.mode != "RGB":
                img = img.convert("RGB")
            img.save(buf, save_fmt, quality=88)
            photo_bytes = buf.getvalue()
        except Exception as e:
            print(f"  warn: photo crop failed for {sp['slug']}: {e}")

        files[f"ppt/media/{img_name}"] = photo_bytes

        # Slide xml + rels
        slide_xml = build_slide_xml(sp, photo_rid="rId4")
        files[f"ppt/slides/slide{slide_num}.xml"] = slide_xml.encode("utf-8")
        files[f"ppt/slides/_rels/slide{slide_num}.xml.rels"] = build_rels_xml(img_name).encode("utf-8")

        # Track presentation rels
        max_rid += 1
        new_slide_rels.append((f"rId{max_rid}", f"slides/slide{slide_num}.xml"))
        new_slide_ids.append((next_sld_id, f"rId{max_rid}"))
        next_sld_id += 1

        # Content types
        ct_xml = ct_xml.replace(
            "</Types>",
            f'<Override PartName="/ppt/slides/slide{slide_num}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>'
        )

    # Update presentation.xml.rels — insert new slide rels before closing tag
    new_rels_xml = "".join(
        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="{tgt}"/>'
        for rid, tgt in new_slide_rels
    )
    pres_rels = pres_rels.replace("</Relationships>", new_rels_xml + "</Relationships>")

    # Update presentation.xml — append new sldId entries
    new_ids_xml = "".join(
        f'<p:sldId id="{sid}" r:id="{rid}"/>' for sid, rid in new_slide_ids
    )
    pres_xml = pres_xml.replace("</p:sldIdLst>", new_ids_xml + "</p:sldIdLst>")

    # Ensure jpg extension is registered in Content_Types
    if 'Extension="jpg"' not in ct_xml:
        ct_xml = ct_xml.replace(
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="jpg" ContentType="image/jpeg"/>'
        )

    files["ppt/_rels/presentation.xml.rels"] = pres_rels.encode("utf-8")
    files["ppt/presentation.xml"] = pres_xml.encode("utf-8")
    files["[Content_Types].xml"] = ct_xml.encode("utf-8")

    # Write output (atomic via temp)
    tmp_out = OUT.with_suffix(".pptx.tmp")
    with zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)
    shutil.move(tmp_out, OUT)
    print(f"Wrote {OUT} with {len(speakers)} speaker slides appended")


if __name__ == "__main__":
    main()
