# Houdini Template Manager <sub>[Django Powered]</sub>

<img src="https://github.com/user-attachments/assets/ff9a257a-c48c-4839-8c60-9db42d36bffe" width="40px">

A Web based application with diverse features to maintain hipfiles and nodes of houdini as bundles 🎁. 
hip file and snippet files saves as ⬇️ ***.hip*** and ***.snip*** respectively

## Houdini Template Publisher

- houdini_template_publisher folder contains modules to execute PySide2 based publisher from Houdini
- pyside2_with_qwwebview.py houdini template manager configured in QWebEngineView to executed from Houdini

## Tech Stack
- Houdini
- PySide2
- PostgreSQL
- Django
- Html, CSS, JS
- Apache HTTP Server


## Model ERD Diagram

- bundles_tag table is many-to-many relation table for connecting single bundle_id has multiple tags

![image](https://github.com/user-attachments/assets/872f6541-f589-4237-83ad-903dc7d87047)

## How To Run 
[have to write]

## How Initial Tables Created  
[have to write]


## Apache Deployments [Windows]

- Goto C:\Windows\System32\drivers\etc
Open hosts file. Write 👇
```
127.0.0.10 houdini-template-manager.com
```

- C:\Apache24\conf\httpd.conf.  Write 👇
```
Listen 127.0.0.10:80

WSGIPythonHome "D:\django_projects"
WSGIPythonPath "D:\django_projects\projects"
LoadFile "C:/Python39/python39.dll"
LoadModule wsgi_module "D:\django_projects\Lib\site-packages\mod_wsgi\server\mod_wsgi.cp39-win_amd64.pyd"
```

- C:\Apache24\conf\extra\httpd-vhosts.conf.  Write 👇

```
<VirtualHost 127.0.0.10:80>
    ServerName houdini-template-manager.com
    ServerAlias houdini-template-manager.com
    ErrorLog "D:\django_projects\projects\houmanager.error.log"
    CustomLog "D:\django_projects\projects\houmanager.access.log" combined

    DocumentRoot "D:\django_projects\projects"
    <Directory D:\django_projects\projects>
        Require all granted
    </Directory>

    <Directory "D:\django_projects\projects">
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    Alias /static "D:\django_projects\projects\central_statics"
    <Directory "D:\django_projects\projects\central_statics">
        Require all granted
    </Directory>

    Alias /media "D:\houdini_bundles"
    <Directory "D:\houdini_bundles">
        Require all granted
    </Directory>

    WSGIScriptAlias / "D:\django_projects\projects\projects\wsgi.py" 
</VirtualHost>
```

- Restart apache server. By running in CMD

```
httpd -k restart
```

Demo Link Below 👇

[![Houdini Template Manger 1.0 Demo Link](https://img.youtube.com/vi/N3YIOAEhO8s/0.jpg)](https://youtu.be/N3YIOAEhO8s)
