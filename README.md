# Houdini Template Manager <sub>[Django Powered]</sub>

<img src="https://github.com/user-attachments/assets/ff9a257a-c48c-4839-8c60-9db42d36bffe" width="45px"> <img src="https://github.com/user-attachments/assets/880b1e30-11bf-4c27-82d3-18cec9694717" width="45px"> <img src="https://github.com/user-attachments/assets/445b01db-9a75-4e03-9806-8a838743c98e" width="45px"> <img src="https://github.com/user-attachments/assets/ac633679-febc-4bf3-b8db-2bcabce0067d" width="45px"> <img src="https://github.com/user-attachments/assets/38ae5696-9a0c-406f-a411-5244e99a81f6" width="45px"> <img src="https://github.com/user-attachments/assets/84d135ee-8045-4ed5-aeeb-b127156155cb" width="45px"> <img src="https://github.com/user-attachments/assets/6399fa00-0e1a-4d36-a9f2-3d0689812a4e" width="45px">

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
- Database tables created manually and migrated using ```python .\manage.py inspectdb > models.py```
- Bundles models class M-to-M created manually ```tag = models.ManyToManyField('Tags', through='BundlesTag')```
  
![image](https://github.com/user-attachments/assets/872f6541-f589-4237-83ad-903dc7d87047)


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
