import os
import subprocess
import zipfile
import html

def escape_code(content):
    return html.escape(content)

def main():
    print("==========================================================")
    print("DevOps Project Report Compiler & Packager")
    print("Student: Vora Gaurang Himanshu")
    print("Email: vora.gaurang2024@vitstudent.ac.in")
    print("==========================================================")

    base_dir = r"c:\Users\gaura\OneDrive\Documents\Devops"
    html_template = os.path.join(base_dir, "report.html")
    html_compiled = os.path.join(base_dir, "report_compiled.html")
    pdf_report_name = "vora.gaurang2024@vitstudent.ac.in_Vora_Gaurang_Himanshu_DevOps_Report.pdf"
    pdf_report_path = os.path.join(base_dir, pdf_report_name)
    zip_name = "vora.gaurang2024@vitstudent.ac.in_Vora_Gaurang_Himanshu_DevOps_Project.zip"
    zip_path = os.path.join(base_dir, zip_name)
    
    # Files to inject into the Appendix
    source_files = [
        ("pom.xml", "corporate-website/pom.xml", "xml"),
        ("App.java", "corporate-website/src/main/java/com/corporate/App.java", "java"),
        ("index.html", "corporate-website/src/main/resources/static/index.html", "html"),
        ("about.html", "corporate-website/src/main/resources/static/about.html", "html"),
        ("services.html", "corporate-website/src/main/resources/static/services.html", "html"),
        ("careers.html", "corporate-website/src/main/resources/static/careers.html", "html"),
        ("gallery.html", "corporate-website/src/main/resources/static/gallery.html", "html"),
        ("contact.html", "corporate-website/src/main/resources/static/contact.html", "html"),
        ("style.css", "corporate-website/src/main/resources/static/css/style.css", "css"),
        ("main.js", "corporate-website/src/main/resources/static/js/main.js", "javascript"),
        ("Dockerfile", "corporate-website/Dockerfile", "dockerfile"),
        ("Jenkinsfile", "corporate-website/Jenkinsfile", "groovy"),
        ("deployment.yaml", "corporate-website/k8s/deployment.yaml", "yaml"),
        ("service.yaml", "corporate-website/k8s/service.yaml", "yaml"),
        ("nagios_services.cfg", "corporate-website/nagios/nagios_services.cfg", "plaintext"),
        ("dashboard.json", "corporate-website/grafana/dashboard.json", "json")
    ]

    print("\n[Step 1/3] Reading project source files for injection...")
    appendix_html = []
    appendix_html.append('<div class="page-break"></div>')
    appendix_html.append('<div class="section">')
    appendix_html.append('  <h2 class="section-header-title">Appendix: Complete Project Source Code</h2>')
    appendix_html.append('  <p>This appendix contains the complete, unedited source code and configurations of the DevOps deployment for ABC Technologies.</p>')

    for title, rel_path, file_type in source_files:
        full_path = os.path.join(base_dir, rel_path)
        if os.path.exists(full_path):
            print(f"Reading {rel_path}...")
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            escaped = escape_code(content)
            appendix_html.append(f'  <h3 class="subsection-title" style="margin-top: 8mm; border-bottom: 1px solid var(--border); padding-bottom: 2px;">{title} (Path: <code>{rel_path}</code>)</h3>')
            appendix_html.append(f'  <pre><code>{escaped}</code></pre>')
        else:
            print(f"[-] Warning: {rel_path} not found.")
            
    appendix_html.append('</div>')
    appendix_code = "\n".join(appendix_html)

    # Read base template and inject appendix before </body>
    print("\nGenerating compiled HTML report...")
    with open(html_template, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    if "</body>" in html_content:
        compiled_content = html_content.replace("</body>", f"{appendix_code}\n</body>")
    else:
        compiled_content = html_content + "\n" + appendix_code

    with open(html_compiled, "w", encoding="utf-8") as f:
        f.write(compiled_content)
    print("[+] Created report_compiled.html")

    # 2. Compile PDF report using Microsoft Edge headless engine
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    print(f"\n[Step 2/3] Compiling single submission PDF using Edge...")
    if not os.path.exists(edge_path):
        print(f"[-] Error: Edge executable not found at {edge_path}")
        return
        
    cmd = [
        edge_path,
        "--headless",
        f"--print-to-pdf={pdf_report_path}",
        "--no-margins",
        html_compiled
    ]
    
    try:
        print(f"Running print-to-pdf command...")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if os.path.exists(pdf_report_path):
            size_kb = os.path.getsize(pdf_report_path) / 1024
            print(f"[+] Success! PDF generated: {pdf_report_name} ({size_kb:.2f} KB)")
        else:
            print("[-] Error: PDF file was not created.")
            return
    except Exception as e:
        print(f"[-] Execution failed: {e}")
        return

    # Clean up compiled HTML
    if os.path.exists(html_compiled):
        os.remove(html_compiled)
        print("Removed temporary compiled HTML file.")

    # 3. Create submission ZIP archive
    print(f"\n[Step 3/3] Creating submission ZIP archive...")
    include_paths = [
        ("corporate-website", True),
        ("screenshots", True),
        (pdf_report_name, False)
    ]
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item, is_dir in include_paths:
                item_full_path = os.path.join(base_dir, item)
                if not os.path.exists(item_full_path):
                    print(f"[-] Warning: Source path {item} does not exist. Skipping.")
                    continue
                    
                if is_dir:
                    print(f"Adding directory: {item}...")
                    for root, dirs, files in os.walk(item_full_path):
                        for file in files:
                            file_full_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_full_path, base_dir)
                            zipf.write(file_full_path, arcname)
                else:
                    print(f"Adding file: {item}...")
                    zipf.write(item_full_path, item)
                    
        zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"[+] Success! ZIP archive created: {zip_name} ({zip_size_mb:.2f} MB)")
    except Exception as e:
        print(f"[-] Failed to write ZIP file: {e}")
        return

    print("\nSubmission Readiness Validation Check:")
    print("----------------------------------------------------------")
    files_to_check = [pdf_report_path, zip_path]
    ready = True
    for f in files_to_check:
        filename = os.path.basename(f)
        if os.path.exists(f):
            print(f"[OK] - File present: {filename} ({os.path.getsize(f)/1024:.1f} KB)")
        else:
            print(f"[MISSING] - File absent: {filename}")
            ready = False
            
    if ready:
        print("----------------------------------------------------------")
        print("[STATUS] - PROJECT IS 100% COMPLETE & READY FOR SUBMISSION!")
        print("==========================================================")

if __name__ == "__main__":
    main()
