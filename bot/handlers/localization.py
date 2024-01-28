class Lang:
    strings = {
        "ru": {
            "start_message": "Привет! Я ваш универсальный бот для управления домом. \n\nЯ помогу вам с оплатой ЖКУ, связью с управляющей компанией и уведомлениями о последних новостях. \n\nВыберите вашу роль, чтобы начать:",

            "news_select_reply": "Выберите нужную вам новость:",
            "user_select_reply": "Выберите нужного вам жителя:",
            "news_select_error": "К сожалению, новостей нет.",
            "user_select_error": "К сожалению, жителей нет.",
            "ticket_select_reply": "Выберите нужную вам заявку:",
            "meter_select_reply": "Выберите нужные вам показания:",
            "ticket_select_error": "На данный момент заявок нет.",
            "news_open_info_error": "Ошибка!\n\nК сожалению, данной новости не существует.",
            "ticket_open_info_error": "Ошибка!\n\nК сожалению, данной заявки не существует.",
            "profile_error": "Ошибка! Профиль не найден.",
            "contact_select_type": 'Выберите тип проблемы, по которой вы хотите обратиться в управляющую компанию',
            "return_to_main_menu": "Вы вернулись в главное меню.",
            "return_to_employer_menu": "Вы вернулись в меню Сотрудника.",
            "return_to_users_menu": "Вы вернулись в меню жителей.",
            "return_to_news_menu": "Вы вернулись в меню новостей.",
            "problem_message": "Тестовое письмо проблемы, которое будет отправлено сотрудникам УК\n\n\nПроблема: {problem_type}\nОписание: {problem_description}",

            "need_registration_error": "Для использования функций программы необходимо зарегистрироваться и дождаться верификации: /start",

            "send_issue_success": "Ваша заявка была успешно отправлена сотруднику Управляющей Компании! \nМы получили ваш запрос и наши специалисты приступили к его рассмотрению. \n\nСпасибо за обращение!",
            "tickets_type_success": "Чтобы увидеть подробности по определенной заявке, нажмите на соответствующую кнопку ниже.",
            "tickets_type_error": "Извините, не удалось найти заявок по данной категории. ",
            "choose_problem_type": "Вы выбрали проблему: {problem}\n\nТеперь опишите подробнее проблему и, при необходимости, прикрепите к сообщению фотографии или видео.",
            "create_news_success": "Новость успешно создана !",
            "employee_access_error": "Извините, у вас нет разрешения на доступ к этой функции.",

            "user_to_ban_error": "Ошибка, пользователя для бана не найден.",
            "close_ticket_error": "Ошибка, заявка для закрытия не найдена.",
            "cancel_ticket_error": "Ошибка, заявка для отмены не найдена.",
            "news_delete_error":"Ошибка, новость для удаления не найдена.",

            "user_is_banned":"Вы были заблокированы в данном боте!",
            "new_users_found_by_complex":"В данном ЖК нету жителей!",
            "user_profile_error":"Профиль пользователя не найден!",
            "meter_no_meters":"Показаний на проверку нет!",
            
        },
        "en": {
            "start_message": "Hello! This is a bot that allows..."
                             "\n\nTo register, please select your role:",
            "news_select_reply": "Select the news you need:",
            "news_select_error": "Unfortunately, there are no news available.",
            "news_open_info_error": "Error!\n\nSorry, this news does not exist.",
            "profile_error": "Error! Profile not found.",
            "contact_select_type": 'Select the type of issue you want to contact the management company about',
            "return_to_main_menu": "You have returned to the main menu.",
            "problem_message": "Test message of the problem that will be sent to UK employees\n\n\nProblem: {problem_type}\nDescription: {problem_description}",
            "need_registration_error": "To use the program's features, you need to register and wait for verification: /start",
            "send_issue_success": "Your request has been successfully sent to the management company employee! We have received your request, and our specialists have started reviewing it. Thank you for contacting us! If you have any questions or additional information, we will contact you as soon as possible.",
            "tickets_type_success": "Here is a list of requests for the selected category.\n\nTo see details about a specific request, click the corresponding button below.",
            "tickets_type_error": "Sorry, we could not find any requests in this category.",
            "choose_problem_type": "You have selected a problem: {problem}\n\nNow describe the problem in more detail and, if necessary, attach photos or videos to the message.",
            "create_news_success": "News created successfully!"
        },
        "uk": {
            "start_message": "Привіт! Це бот, який дозволяє..."
                             "\n\nДля реєстрації оберіть свою роль, будь ласка:",
            "news_select_reply": "Оберіть потрібну вам новину:",
            "news_select_error": "На жаль, новин немає.",
            "news_open_info_error": "Помилка!\n\nНа жаль, цієї новини не існує.",
            "profile_error": "Помилка! Профіль не знайдено.",
            "contact_select_type": 'Оберіть тип проблеми, з якою ви хочете звернутися до управлінської компанії',
            "return_to_main_menu": "Ви повернулися в головне меню.",
            "problem_message": "Тестове повідомлення про проблему, яке буде відправлено співробітникам УК\n\n\nПроблема: {problem_type}\nОпис: {problem_description}",
            "need_registration_error": "Для використання функцій програми необхідно зареєструватися та дочекатися верифікації: /start",
            "send_issue_success": "Ваш запит успішно відправлено співробітнику Управлінської Компанії! Ми отримали ваш запит, і наші спеціалісти розпочали його розгляд. Дякуємо за звернення! Якщо у вас виникнуть питання чи додаткова інформація, ми зв'яжемося з вами найближчим часом.",
            "tickets_type_success": "Ось список заявок за обраною категорією.\n\nЩоб переглянути деталі щодо певного запиту, натисніть відповідну кнопку нижче.",
            "tickets_type_error": "Вибачте, не вдалося знайти жодних заявок за цією категорією.",
            "choose_problem_type": "Ви обрали проблему: {problem}\n\nТепер детальніше опишіть проблему, а за необхідності додайте до повідомлення фотографії або відео.",
            "create_news_success": "Новина успішно створена!"
        },
        "de": {
            "start_message": "Hallo! Das ist ein Bot, der es ermöglicht..."
                             "\n\nUm sich zu registrieren, wählen Sie bitte Ihre Rolle:",
            "news_select_reply": "Wählen Sie die gewünschte Nachricht:",
            "news_select_error": "Leider gibt es keine Nachrichten.",
            "news_open_info_error": "Fehler!\n\nLeider existiert diese Nachricht nicht.",
            "profile_error": "Fehler! Profil nicht gefunden.",
            "contact_select_type": 'Wählen Sie den Typ des Problems aus, zu dem Sie sich an das Management-Unternehmen wenden möchten',
            "return_to_main_menu": "Sie sind zum Hauptmenü zurückgekehrt.",
            "problem_message": "Testnachricht des Problems, die an die Mitarbeiter des UK gesendet wird\n\n\nProblem: {problem_type}\nBeschreibung: {problem_description}",
            "need_registration_error": "Um die Funktionen des Programms zu nutzen, müssen Sie sich registrieren und auf die Verifizierung warten: /start",
            "send_issue_success": "Ihre Anfrage wurde erfolgreich an einen Mitarbeiter des Managementunternehmens gesendet! Wir haben Ihre Anfrage erhalten, und unsere Spezialisten haben mit der Prüfung begonnen. Vielen Dank für Ihre Anfrage! Bei Fragen oder zusätzlichen Informationen werden wir uns so schnell wie möglich bei Ihnen melden.",
            "tickets_type_success": "Hier ist eine Liste von Anfragen für die ausgewählte Kategorie.\n\nUm Details zu einer bestimmten Anfrage anzuzeigen, klicken Sie auf die entsprechende Schaltfläche unten.",
            "tickets_type_error": "Entschuldigung, wir konnten keine Anfragen in dieser Kategorie finden.",
            "choose_problem_type": "Sie haben ein Problem ausgewählt: {problem}\n\nBeschreiben Sie das Problem jetzt genauer und fügen Sie bei Bedarf Fotos oder Videos zur Nachricht hinzu.",
            "create_news_success": "Nachricht erfolgreich erstellt!"
        },
        "sr": {  
            "start_message": "Поздрав! Ја сам ваш универзални бот за управљање кућом. \n\nПомоћи ћу вам са плаћањем комуналних услуга, комуникацијом са управом и обавештењима о последњим вестима. \n\nИзаберите вашу улогу да бисте почели:",
            "news_select_reply": "Изаберите жељену вест:",
            "news_select_error": "На жалост, нема вести.",
            "ticket_select_reply": "Изаберите жељени тикет:",
            "ticket_select_error": "На жалост, нема тикета.",
            "news_open_info_error": "Грешка!\n\nНа жалост, ова вест не постоји.",
            "ticket_open_info_error": "Грешка!\n\nНа жалост, овај тикет не постоји.",
            "profile_error": "Грешка! Профил није пронађен.",
            "contact_select_type": 'Изаберите тип проблема за који желите обратити управу',
            "return_to_main_menu": "Вратили сте се на главни мени.",
            "problem_message": "Тест порука о проблему која ће бити послата запосленима у Управи \n\n\nПроблем: {problem_type}\nОпис: {problem_description}",
            "need_registration_error": "За коришћење функција програма, потребно је регистровати се и сачекати верификацију: /start",
            "send_issue_success": "Ваш тикет је успешно послат запосленом у Управи Компаније! \nПримили смо ваш захтев и наши стручњаци су почели са његовим разматрањем. \n\nХвала вам на обраћању!",
            "tickets_type_success": "Да бисте видели детаље о одређеном тикету, притисните одговарајуће дугме испод.",
            "tickets_type_error": "Извините, није успело пронаћи тикете за ову категорију. ",
            "choose_problem_type": "Изабрали сте проблем: {problem}\n\nСада детаљно опишите проблем и, по потреби, приложите фотографије или видео поруке.",
            "create_news_success": "Вест је успешно креирана!",
            "employee_access_error": "Извините, немате дозволу за приступ овој функцији."
        }
    }


def get_localized_message(language_code, key, **kwargs):
    if language_code in Lang.strings and key in Lang.strings[language_code]:
        message_template = Lang.strings[language_code][key]
        return message_template.format(**kwargs)
    else:
        return f"Translation not found for key '{key}' in language '{language_code}'"
