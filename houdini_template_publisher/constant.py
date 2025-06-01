SNAPSHOT_DISABLE = FILE_BROWSER_BUTTON_DISABLE= f"""
    QPushButton {{
        border: none;
        background: none;
        color: none;
    }}
"""
IS_NODE_SNIPPET_DISABLE = IS_TEMPLATE_DISABLE =f"""
    QCheckBox{{
            color: rgb(149, 149, 149);
            font-family: "Asap";
            font: bold;
            font-size:17px;
        }}
"""
CONTEXT_DISABLE = CATEGORY_DISABLE= f"""
    QComboBox {{
        background-color: rgb(149, 149, 149);
        border: 1px solid #a0a0a0;
        border-radius: 3px;
        padding: 5px;
        padding-left: 10px;
        color: #333333;
        min-width: 6em;
        font-size: 17px;
    }}
"""

IMG_PATH_DISABLE = f"""
    QTextEdit {{
        background-color: rgb(149, 149, 149);
        border: 1px solid #a0a0a0;
        border-radius: 3px;
        color: black;
        font-family: "Asap";
        font-size: 17px;
    }}
"""

CATEGORY_ENABLE = CONTEXT_ENABLE= f"""
    QComboBox {{
        background-color: #e0e0e0;
        border: 1px solid #a0a0a0;
        border-radius: 3px;
        padding: 5px;
        padding-left: 10px;
        color: #333333;
        min-width: 6em;
        font-size: 17px;
    }}

    QComboBox:hover {{
        background-color: #d0d0d0;
        border-color: #909090;
    }}

    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;

    }}

    QComboBox::down-arrow {{
        image: url("D:/houdini_template_publisher/icons/arrow-down-3101.svg");
        width: 2px;
        height: 2px;
    }}

    QComboBox QAbstractItemView {{
        background-color: #e0e0e0;
        border: 1px solid #a0a0a0;
        selection-background-color: #c0c0c0;
        color: #333333;
        outline: none;
    }}

    QComboBox QAbstractItemView::item {{
        padding: 5px;
        padding-left: 10px;
    }}

    QComboBox QAbstractItemView::item:hover {{
        background-color: #d0d0d0;
    }}

    QComboBox QAbstractItemView::item:selected {{
        background-color: #c0c0c0;
    }}
"""

IMG_PATH_ENABLE = f"""
        QTextEdit {{
            background-color: #e0e0e0;
            border: 1px solid #a0a0a0;
            border-radius: 3px;
            color: black;
            font-family: "Asap";
            font-size: 17px;
        }}
"""

SNAPSHOT_ENABLE = f"""
    QPushButton {{
        background-color: rgb(0, 20, 84); 
        color: white;
        border: none;
        border-radius: 50%; 
        font-size: 17px;
        font-weight: bold;
    }}

    QPushButton:hover {{
        background-color:  #2e3138; 
    }}
    
    QPushButton:pressed {{
        background-color: #2A56C6; 
    }}
"""

IS_NODE_SNIPPET_ENABLE = IS_TEMPLATE_ENABLE= f"""
    QCheckBox {{
            color: #fff;
            font-family: "Asap";
            font: bold;
            font-size:17px;
        }}
"""

FILE_BROWSER_BUTTON_ENABLE= f"""
QPushButton {{
            background-color:rgb(127, 134, 150);  /* Google blue */
            color: white;
            border: none;
            border-radius: 50%;  /* Circular button */
            
            font-size: 17px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color:  rgb(90, 112, 89);  /* Slightly darker blue */
        }}
        
        QPushButton:pressed {{
            background-color: #2A56C6;  /* Even darker blue */
        }}
"""

##################################################################
TEMPLATE_BUNDLE_PATH = r"D:\houdini_bundles"