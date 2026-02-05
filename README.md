# MegaSchool
## Authors:
- Semenov Vlad
- Vinogradov Ivan
## Description:
An application for schemes (flowchart) recognition.
## Project structure:
- `app.py` - main python file, performing development server execution and containing every route's description
- `templates\` - Jinja2 html templates
- `static\` - css and js files
- `model\` - a folder containing YOLO weighs files, images used to train the model and a module including functions to interact with YOLO
- `model\scheme_scanner.py` - function `getTokens()` receives a path to flowchart image and retrieves formatted geometrical tokens 
- `alg_utils\` - a folder containing logic for transforming tokens into text algorithm
- `alg_utils\alg_writer.py` - main file presenting `constructFromTree()` and `constructFromImage()` functions. Both of them give back text algorithms, but the former requires tree object to work with whereas the latter needs only the picture of scheme itself.
- `uploads\` - a folder for all kind of files uploaded to the server
- `writtenAlgs\` - a folder for all algorithms got with `alg_utils\alg_writer.py`
## How to run the app?
- Install all the libraries listed in `requirements.txt`:
```commandline
pip install -r requirements.txt
```
- Set the working directory to the root of the repo
- Run `app.py` file with no parameters