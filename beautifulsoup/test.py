string = "Adaptor 100W\nAdaptor 240W\nStylus (ASUS Pen SA203-MPP2.0 support)"

if '\n' in string:
    value = string.strip().split('\n')
    
print(value)