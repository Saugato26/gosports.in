#!/usr/bin/env bash
# Pull reusable images from gosports.in (WordPress uploads) into assets/img/live/<category>/
# Tries the original upload first (suffix -WxH / -scaled stripped), falls back to the referenced size.
set -u
B="https://gosports.in/wp-content/uploads"
cd "$(dirname "$0")"
ok=0; fb=0; miss=0
get() { # category  path
  local cat="$1" p="$2" dir="assets/img/live/$1" name orig
  mkdir -p "$dir"
  name="$(basename "$p")"
  orig="$(echo "$p" | sed -E 's/-[0-9]+x[0-9]+(\.[a-z]+)$/\1/; s/-scaled(\.[a-z]+)$/\1/')"
  local oname; oname="$(basename "$orig")"
  if [ "$orig" != "$p" ] && curl -sfL --max-time 30 -o "$dir/$oname" "$B/$orig"; then
    echo "orig  $cat/$oname"; ok=$((ok+1))
  elif curl -sfL --max-time 30 -o "$dir/$name" "$B/$p"; then
    echo "ref   $cat/$name"; fb=$((fb+1))
  else
    echo "MISS  $p"; miss=$((miss+1)); rm -f "$dir/$name" "$dir/$oname"
  fi
}
# --- brand ---
for p in 2025/12/white-logo.svg 2025/12/black-gosports.png 2025/12/Logo.svg 2025/12/red-background-pattern.svg 2025/12/Website-pattern-2.svg 2026/01/Vector.svg 2025/12/cta-bg-image-scaled.png; do get brand "$p"; done
# --- programme logos ---
for p in 2026/06/Aspire-logo.png 2026/06/CMACEA-logo.png 2026/05/GFG-2025-LOGO-03.png 2026/06/Mrtss-logo.png 2026/05/PCP-logo-scaled.jpg 2026/06/Rcb-logo-website.png 2026/06/Samarth-logo.png 2026/06/TJK-logo.png 2026/06/Ubhar-logo.png 2026/03/Gear-for-Gold-logo-asset-for-programme-page-scaled.jpg 2026/03/infy-logo-2025-website--scaled.png; do get programme-logos "$p"; done
# --- photography ---
for p in 2026/05/DSC04871-2048x1537.jpg 2026/05/WhatsApp-Image-2026-05-04-at-18.04.25-2048x1363.jpeg 2026/05/ZNP06359-scaled.jpg 2026/03/ZNP06357-1024x683.jpg 2026/05/15-19-15-2048x1333.jpg 2026/05/15-19-16-2048x1333.jpg 2026/05/15-19-17-2048x1333.jpg 2026/05/15-19-18-2048x1333.jpg 2026/05/15-19-19-2048x1333.jpg 2026/05/LAHA1719-2048x1365.jpg; do get photography "$p"; done
# --- hero / section backgrounds ---
for p in 2026/05/Home-Page-1-1024x548.png 2026/05/Home-Page-2-1024x563.png 2026/05/Home-page-3-1024x560.png 2026/05/Home-page-5.png-1.jpg 2026/05/Home-page-6.png-2.jpg 2026/05/Home-page-bg-1.jpg 2026/07/3-Sapa-centre-image-slider.jpg 2026/05/Get-Involved-Hero-Banner-2-1024x576.jpg 2025/11/video-image-2048x996.png 2025/12/pillars-bg-image-2048x970.png 2025/12/Image.png 2025/12/career-hero-1024x330.png 2025/12/donation-image-1024x233.png; do get heroes "$p"; done
# --- trustees & board ---
for p in 2026/05/Untitled-8.png 2026/05/Gopi.png.webp 2025/12/nandan.png 2026/05/Thomas.png 2026/05/Abishek.png 2026/05/Umnish.png 2026/06/Meghana-Final.png 2026/06/Deepthi.png 2026/08/Desh-2048x2048.jpg 2025/12/john.png 2026/06/Sree-2048x2048.jpg 2026/06/Ajay-2048x2048.jpg; do get board "$p"; done
# --- team ---
for p in 2026/06/Saugato.jpg.jpeg 2025/12/Sonali-2048x2048.jpg 2025/12/nayar.png 2025/12/sajiv.png 2026/06/raghv-scaled.jpg 2026/06/Hasan.jpg 2025/12/profile-image.png 2026/06/Suraj.jpg 2026/06/Ajanth-scaled.jpg 2026/06/Karan-scaled.jpg 2026/06/Anirban-scaled.jpg 2026/06/Vipul--scaled.jpg 2026/06/Samyukth.jpg 2026/06/Sahil.jpg; do get team "$p"; done
# --- testimonials ---
for p in 2026/05/Sumit-Photo-video.jpg 2026/05/Ashwini-Photo-website.jpg 2026/05/Falak-website-photo.jpg 2026/05/Shruthi-Photo-website.jpg 2026/05/Testi-5.jpg; do get testimonials "$p"; done
# --- awards ---
for p in 2026/05/Award-NATIONAL-2048x2013.jpg 2025/12/Image-1.png 2026/05/Award-2-2048x2013.jpg 2026/05/Award-1-2048x2013.jpg 2026/05/Award-3-2048x2013.jpg 2026/05/Award-4.jpg; do get awards "$p"; done
# --- partner logos: 34 from home (1024x561) ---
for p in Logo-1 Logo-2 Logo-3 Logo-4 Logo-5 Logo-6 Logo-7 Logo-8 Logo-9 Logo-10-11-16 Logo-10-11-17 Logo-12-15-18 Logo-12-15-19 Logo-12-15-20 Logo-16-18-21 Logo-16-18-22 Logo-16-18-23 Logo-19-21-24 Logo-19-21-25 Logo-19-21-26 Logo-27-30-27 Logo-27-30-28 Logo-27-30-29 Logo-30-34-30 Logo-30-34-31 Logo-30-34-32 Logo-30-34-33 Logo-30-34-34 Logo-35-38-35 Logo-35-38-36 Logo-35-38-37 Logo-35-38-38; do get partners-home "2026/05/$p.jpg"; done
get partners-home 2025/12/RCB.png
# --- partner logos: 27 from get-involved (292x160 png) ---
for p in infosys fusion AtT RCB capital bridge-foundation booking deloitte-logo indusind-bank skechers husys sports herbalife sportz gameskraft BI-worldwide moving-together mangal infogain fdc-limited amm-foundation mvs one; do get partners-getinvolved "2025/12/$p.png"; done
echo; echo "originals: $ok   referenced-size: $fb   missing: $miss"
echo "total files: $(find assets/img/live -type f | wc -l)   size: $(du -sh assets/img/live | cut -f1)"
