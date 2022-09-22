# Tutorial to make a pdf with django


## Things to do before start
We are going to work with wkhtmltopdf and pdfkit, so we need to do the following things in oder to start working.

**First of all, we need to download everything**

1. Do this if you use windows
    * Download [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html), download the one you need.
    * Follow the installation wizard.
2. Do this if you use linux
   * Run the following command `sudo apt-get install wkhtmltopdf`
  
## First steps

1. Install pdfkit with the following command `pip|pip3 install pdfkit`
2. If you want to creare QR codes use `pip|pip3 install pyqrcode` and `pip|pip3 install pypng`, pypng is used to save qr as png and as base64
3. In your app, create a folder named, "utils".
4. Inside of it, create a python file named, "utils.py" or "reports.py".

### Inside your file
Several things are needed to create the pdf script, you need:
1. Function or functions to get the data to print on report (This is not needed, but it is recommended, just to be clear) see [block of code 1](#example-of-function-to-get-data).
2. Import abosolute path from django settings or write a function to get it (optional but recommended) see [block of code 2](#path-to-import-absolute-path-from-django).
3. Create your main function to generate the pdf, see [block of code 3](#example-of-main-function-to-create-a-pdf).


#### Example of function to get data
```python
from apps.exampleapp.modesl import Model


def get_data(pk:int, request, info_you_need):
    # Do things
    example = Model.objects.filter(id=id)

    # Example of creating a qr
    # Url for QR
    url = 'https://www.google.com/maps/'
    # Create the qrcode and save it as base64
    qr = pyqrcode.create(url).png_as_base64_str(scale = 5) # Scale is the size of qr
    # If you want to add a qr to an object just do the following
    # setattr(object, 'qr', qr)

    # make more things
    data = {
        'example': example,
        # More info
    }
    return data

```


#### Example of function to get absolute function

##### Function to get absolute path example
```python
from pathlib import Path


def get_absolute_path():
    return Path(__file__).parent.resolve()

```

##### Path to import absolute path from django

```python
from django.conf.settings import BASE_DIR
# or
from django.conf import settings # Here you can import almost every thing in settings.py
```


#### Example of main function to create a pdf
```python
# Django things
from django.shortcuts import render
from django.template.loader import get_template
from django.conf import settings

# Own things


# Third party things
import pdfkit

# Python things
import platform

def generate_pdf(pk, template_name:str, request, info_you_need):
    # Get the data
    data = get_data(pk, request = request)
    # Get the template
    template = get_template(template_name)
    # Render the data in the template
    html = template.render(data)
    
    # options to config pdfkit
    options = {
        "page-size": 'Letter', # Page size 
        'title': "PDF title", # File title
        #'margin-top': '200px', # Margin top
        #'margin-right': '0px', # Margin right
        #'margin-left': '0px', # Margin left
        #'margin-bottom': '10px', # Margin botton
        'encoding': "ISO-8859-3", # File enconding, it can be UTF-8 but sometimes it does not work
        #'footer-html': 'templates/footer.html', # Footer
        #'--header-html': 'templates/header.html', # Header
        #'--header-spacing': '-223', # Header spacing from the content
        #'--footer-spacing': '-14', # Footer spacing from the content
        '--enable-local-file-access': "", # The pdf can access file from the local machine
    }
    
    # Config of wkhtmltopdf
    # Default is linux config else windows config
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf') \
        if platform.system() != 'Windows' \
        else pdfkit.configuration(
            # Windows config
            wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )
    # This is the path to the css
    # STATICFILES_DIRS[0] are the dirs to access the static files like js, css and images, css mus be load here or using cdn in html
    css = [
        f'{settings.STATICFILES_DIRS[0]}/assets/css/styles.min.css', 
        f'{settings.STATICFILES_DIRS[0]}/assets/bootstrap/css/bootstrap.min.css',
        # etc
    ]
    
    # Generate the pdf from string using the rendered html, the options and the config, we can add the css, and write the path to save it, 
    # in this case is not saved, it is just rendered miau
    # to add css just write css=css and the save path is output_path='miau.pdf'
    pdf_file = pdfkit.from_string(html, options=options, configuration=config, css=css)
    
    return pdf_file
```