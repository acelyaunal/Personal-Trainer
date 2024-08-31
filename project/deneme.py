import os

templates_dir = os.path.join(os.getcwd(), 'templates')
template_file = 'select_exercises.html'

if os.path.exists(os.path.join(templates_dir, template_file)):
    print("Dosya bulundu.")
else:
    print("Dosya bulunamadı.")
