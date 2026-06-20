import json
import os
from jinja2 import Environment, FileSystemLoader
from utils.logger import LOGGER

def generate_html(results: dict, output_dir: str) -> str:
    """Generate a human-readable HTML report"""
    env = Environment(loader=FileSystemLoader("modules/reporting/templates"))
    template = env.get_template("report.html")
    html_content = template.render(results=results)

    output_path = os.path.join(output_dir, "sayanox_report.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return output_path

def generate_json(results: dict, output_dir: str) -> str:
    """Generate a machine-readable JSON report"""
    output_path = os.path.join(output_dir, "sayanox_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    return output_path

def generate(results: dict, output_dir: str, config: dict) -> None:
    """Main function to generate all requested report formats"""
    os.makedirs(output_dir, exist_ok=True)
    for fmt in config["reporting"]["formats"]:
        if fmt.lower() == "html":
            path = generate_html(results, output_dir)
        elif fmt.lower() == "json":
            path = generate_json(results, output_dir)
        LOGGER.info(f"Generated {fmt.upper()} report: {path}")
      
