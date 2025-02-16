# Papyrus 📜

CLI tool that generates an OpenAPI documentation from your Pyramid application. 
Designed to get you up and running fast with minimal fuss.

---

## ✨ Features

- **Automated OpenAPI Docs:** Generate up-to-date API documentation from your Pyramid app automatically.
- **Flexible Output:** 
  - **Clipboard:** Pipe the output to your clipboard (e.g., using `pbcopy` on macOS).
  - **File:** Redirect output to a file (e.g., `api.yml`).
- **Intuitive CLI:** Built with [Typer](https://typer.tiangolo.com/) for a smooth command-line experience.


## ⚙️ Requirements

- **Python:** Version 3.13 or higher.


## 📦 Installation

Install Papyrus via the UV tool:

```bash
uv tool install git+https://github.com/iamlucasvieira/papyrus
```
Or clone the repository and install manually:

```bash
git clone https://github.com/iamlucasvieira/papyrus
cd papyrus
pip install .
```

## 🚀 Usage
### 1. Navigate to Your Pyramid App <br>
Go to the directory of your Pyramid app (the directory containing your `routes.py`):
```bash
  cd /path/to/your/pyramid/app
  ```
### 2. Run Papyrus<br>
Execute the command to generate the OpenAPI documentation:
```bash
papyrus
```

### 3. Output Options
   
Copy to Clipboard: Pipe the output directly to your clipboard (macOS example):
```bash
papyrus | pbcopy
```

Save to a File: Redirect the output to save it as a YAML file:
```bash
papyrus > api.yml
```

## 🤝 Contributing
Contributions are always welcome!
If you have ideas for improvements or spot any issues, please open an issue or submit a pull request.

## 📄 License
Distributed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🙏 Acknowledgements
A big thank you to the maintainers of these awesome tools that make Papyrus possible:
- [typer](https://github.com/tiangolo/typer)
- [cattrs](https://github.com/python-attrs/cattrs)
- [rich](https://github.com/Textualize/rich)
- [openapi-spec-validator](https://github.com/p1c2u/openapi-spec-validator)
