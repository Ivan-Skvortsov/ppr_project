from docxtpl import DocxTemplate

context = {
    'facility_name': 'ГПА-11',
    'day': 10,
    'month': 'Июля',
    'year': 2021,
    # 'remarks': 'Сюда пишем замечания!',
    'employee1': 'Инженер АСУ, А и ТМ',
    'name1': 'Сидоров Т.П.',
    'employee2': 'Приборист',
    'name2': 'Смирнов Г.В.',
    'employee3': None,
    'name3': None,
    'row_contents': [
        {
            'desc': 'Yokogawa EJA530',
            'q': 10,
            't': 'TO-2',
            'p': '38, 39'
        },
        {
            'desc': 'Метран-150',
            'q': 15,
            't': 'TO-4',
            'p': '11'
        },
        {
            'desc': 'Садко-103',
            'q': 3,
            't': 'TO-3',
            'p': '2'
        }

    ]
}

target_file = r'/mnt/d/Dev/ppr_project/output/gpa_vse_vzo.docx'
template_file = r'/mnt/d/Dev/ppr_project/templates/gpa_vse_vzo.docx'

docx_template = DocxTemplate(template_file)
print(target_file)
docx_template.render(context=context)
docx_template.save(target_file)
