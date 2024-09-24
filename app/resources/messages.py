message_welcome = (
    "Добро пожаловать в Telegram-бота, автоматизирующего "
    "процессы управления графиком и персоналом.\n\n<b>Перед "
    "началом работы необходимо узнать кто Вы?</b>"
)

message_menu_manage_company = "<b>Управление компаниями</b>\n\nЗдесь отображаются созданные Вами компании."

message_menu_delete_manage_company = "<b>Управление компаниями</b> \n\nНеобходимо выбрать компанию которую хотите удалить."

message_create_company = ("<b>Создание компании</b>\n\nДля того чтобы создать новую компанию в данном Telegram-боте, "
                          "необходимо заполнить"
                          "некоторые данные.")

message_delete_company = "<b>Компания успешно удалена!</b>"
message_employee_already_join = "<b>Вы уже являетесь сотрудником данной компании!</b>"
message_employee_join = "<b>Сотрудники компании</b>\n\nПо Вашей ссылке в компанию был добавлен сотрудник, убедитесь что это тот кто вам нужен, в противном случае удалите его с компании"

word_button_employer = "Работодатель 💼"
word_button_employee = "Работник 🗓"

message_button_start_create_company = "Начать создание"
message_button_create_company = "Создать компанию"
message_button_delete_company = "Удалить компанию"
message_button_back = "Вернуться назад ⬅"
message_data_was_add = "<b>Данные успешно добавлены!</b>"
message_data_was_update = "<b>Данные успешно обновлены!</b>"
message_data_was_error = "<b>Данные не записали! Повторите попытку позже!</b>"

message_use_keyboard = "Для управления данной компанией используйте кнопки на вашей клавиатуре!"

message_enter_company_name = (
    "<i><b>Введите название вашей компании:</b></i>"
    "\n\nТут необходимо ввести название "
    "вашей компании или название сети "
    "компаний в целом. Например: Яндекс ПВЗ."
)

message_enter_company_adress = (
    "<i><b>Введите адрес вашей компании:</b></i>"
    "\n\nПросто введите краткий адрес работы, "
    "это необходимо чтобы прикрепить сотрудника"
    "к определенному адресу."
)

message_enter_company_type_of_activity = (
    "<i><b>Введите вид деятельности вашей компании:</b></i>"
    "\n\nДополнительная статистическая инфомация, "
    "можете написать сюда что угодно, но будет приятно"
    "если укажете настоящий род деятельности!"
)

message_enter_manager_name = (
    "<i><b>Введите ваше Фамилию Имя Отчество</b></i>"
    "\n\nЭти данные будут видны работникам компании по адресу"
    "для того чтобы знать кто Вы и как к Вам обращаться."
)

message_enter_manager_phone = (
    "<i><b>Введите ваш номер телефона</b></i>"
    "\n\nЭта информация нужна для связи сотрудников с "
    "вами в экстренных случаях, для того чтобы не было"
    "лишних проблем стоит указать номер."
)

message_enter_manager_post = (
    "<i><b>Введите вашу должность в компании:</b></i>"
    "\n\nЭту информацию будут видеть сотрудники "
    "компании по адресу, необходимо для того чтобы "
    "сотрудники понимали к кому обращаются"
)

message_enter_full_name = ("<b>Пожалуйста введите свое ФИО</b>\n\n"
                           "Необходимо ввести полностью фио, эти "
                           "данные будут видны только работодателю!"
                           )

message_enter_age = ("<b>Пожалуйста введите свой возраст</b>\n\n"
                     "Необходимо ввести ваш текущий полный возраст. Например: 18, эти данные будут видны только "
                     "работодателю!"
                     )

message_enter_phone = ("<b>Пожалуйста введите свой номер телефона</b>\n\n"
                       "Необходимо ввести номер телефона в формате: 89991234567, "
                       "эти данные будут видны только работодателю!"
                       )

message_enter_bank = ("<b>Пожалуйста введите название банка</b>\n\n"
                      "Необходимо ввести название банка для того "
                      "чтобы перечилять зп, эти данные будут видны "
                      "только работадателю!"
                      )

message_enter_schedule = (f"<b>Введите тип графика комапнии</b>\n\n"
                          f"5/2, 6/1, ежедневно"
                          )

message_enter_startday = (f"<b>Введите с какого дня будет сгенерирован график</b>\n\n"
                          f"Используйте формат числа. Например: 9 - то есть с 9 числа каждого месяца будет "
                          f"генерироваться график")

message_enter_endday = (f"<b>Введите по какой день будет сгенерирован график</b>\n\n"
                        f"Используйте формат числа. Например: 25 - то есть по 25 число каждого месяца будет "
                        f"генерироваться график")

message_enter_charttime = (f"<b>Введите время работы компании</b>\n\n"
                           f"Используйте формат типа 09:00-21:00")

message_enter_payrephouse = (f"<b>Введите оплату за час работы компании</b>\n\n"
                             f"Используйте формат 120.0")

message_enter_paymentforoverfulfillment = (f"<b>Оплачивается ли излишки за час работы компании</b>\n\n"
                                           f"Используйте формат Да/Нет\n"
                                           f"Да - если работник задержится тогда это будет учитыватся\n"
                                           f"Нет - если не учитывается время задержки после работы")

message_enter_premium = (f"<b>Есть ли премия за работу в компании</b>\n\n"
                         f"Используйте формат Да/Нет\n"
                         f"Да - если есть премии\n"
                         f"Нет - если нет премии")

message_company_already_create = "<b>Компания уже была создана, попробуйте изменить некоторые данные! </b>"
message_company_not_selected = ("<b>Компания не выбрана!</b>\n\n"
                                "Пожалуйста нажмите в меню компании "
                                "на одну из предложенных или нажмите на"
                                "клавиатуре Сменить компанию и управляйте ей!")


async def message_get_invite(company_name: str, company_address: str):
    return ("Добро пожаловать в Telegram-бота, автоматизирующего процессы управления графиком и персоналом.\n\n"
            "<b>Вы были приглашены в компанию!</b>\n\n"
            "Название компании:\n"
            f"└<b>{company_name}</b>\n\n"
            "Адрес компании:\n"
            f"└<b>{company_address}</b>\n\n"
            )


async def message_company_was_created(company_id: int, company_name: str, company_address: str, company_type_of_activity: str,
                                      company_manager_name: str, company_manager_phone: str, company_manager_post: str):
    return ("Индефикатор компании:\n" + f"└<b>{company_id}</b>\n\n" +
            "Название компании:\n" + f"└<b>{company_name}</b>\n\n" +
            "Адрес компании:\n" + f"└<b>{company_address}</b>\n\n" +
            "Вид деятельности:\n" + f"└<b>{company_type_of_activity}</b>\n\n" +
            "Фамилия Имя Отчество:\n" + f"└<b>{company_manager_name}</b>\n\n" +
            "Номер телефона:\n" + f"└<b>{company_manager_phone}</b>\n\n" +
            "Должность в компании:\n" + f"└<b>{company_manager_post}</b>\n\n" +
            "Компания успешно создалась!")


async def message_short_info_company(company_id: int, company_name: str, company_address: str, company_type_of_activity: str):
    return (
            "<b>Управление компанией:</b>\n\n" +
            "Индефикатор компании:\n" + f"└<b>{company_id}</b>\n\n" +
            "Название компании:\n" + f"└<b>{company_name}</b>\n\n" +
            "Адрес компании:\n" + f"└<b>{company_address}</b>\n\n" +
            "Вид деятельности:\n" + f"└<b>{company_type_of_activity}</b>\n\n"
    )


async def message_data_schedule_not_exists(company_address: str):
    return (
            f"График для компании с адресом {company_address}\n\n" +
            f"Данные отсутствуют, пожалуйста заполните их!"
    )


async def message_schedule_data(company_address: str, company_chart: str, company_chart_time: str,
                                number_of_hours_per_shift: int, payment_per_hour: float,
                                payment_for_over_fulfillment: bool, premium: bool, start_date_shift: str,
                                end_date_shift: str):
    return (f"<b>График компании</b>\n└{company_address}\n\n"
            f"График работы:\n" + f"└<b>{company_chart}  {company_chart_time}</b>\n\n" +
            f"Количество часов в смене:\n" + f"└<b>{number_of_hours_per_shift}</b>\n\n" +
            f"Оплата за час работы:\n" + f"└<b>{payment_per_hour}</b>\n\n" +
            f"Оплата за переизбыток часов:\n" + f"└<b>{'Да' if payment_for_over_fulfillment else 'Нет'}</b>\n\n" +
            f"Оплата премий:\n" + f"└<b>{'Да' if premium else 'Нет'}</b>\n\n"
                                  f"Составление графика:\n" + f"└<b>с {start_date_shift} по {end_date_shift}</b>"
            )


async def message_employee_data(company_address: str, count_employee, current_company_id: int):
    return (f"<b>Сотрудники компании</b>\n"
            f"└{company_address}\n\n"
            f"Количество сотрудников\n"
            f"└{await count_employee(
                company_id=current_company_id
            )}"
            )


async def message_short_info_employee(employee_id: int, company_address: str, start_date_work: str, full_name: str,
                                      age: int, phone: str, bank: str):
    return (f"Индефикатор сотрудника\n"
            f"└{employee_id}\n\n"
            f"Адрес работы\n"
            f"└{company_address}\n\n"
            f"Начал работать\n"
            f"└{start_date_work}\n\n"
            f"Фамилия Имя Отчество\n"
            f"└{full_name}\n\n"
            f"Возраст\n"
            f"└{age}\n\n"
            f"Номер телефона\n"
            f"└{phone}\n\n"
            f"Используемый банк\n"
            f"└{bank}")


async def message_referral_link(company_id: int):
    return (f"<b>Пригласительная ссылка</b>\n\n"
            f"Данная ссылка может использоваться для нескольких сотрудников\n"
            f"https://t.me/workRoster_bot?start={company_id}"
            )
