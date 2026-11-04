from datetime import datetime

from clinic.service import ClinicService


def main():
    clinic = ClinicService()

    while True:
        print("\n=== Поліклініка ===")
        print("1 — Додати лікаря")
        print("2 — Додати пацієнта")
        print("3 — Записати на прийом")
        print("4 — Позначити відвідування")
        print("0 — Вийти")

        choice = input("Оберіть дію: ").strip()

        try:
            if choice == "1":
                name = input("Ім'я лікаря: ")
                specialty = input("Спеціальність: ")
                doctor = clinic.add_doctor(name, specialty)
                print(f"Лікаря додано. ID: {doctor.id}")

            elif choice == "2":
                name = input("Ім'я пацієнта: ")
                patient = clinic.add_patient(name)
                print(f"Пацієнта додано. ID: {patient.id}")

            elif choice == "3":
                doctor_id = int(input("ID лікаря: "))
                patient_id = int(input("ID пацієнта: "))
                date_text = input("Дата й час (РРРР-ММ-ДД ГГ:ХХ): ")
                starts_at = datetime.strptime(date_text, "%Y-%m-%d %H:%M")

                appointment = clinic.book_appointment(
                    doctor_id, patient_id, starts_at
                )
                print(f"Запис створено. ID: {appointment.id}")

            elif choice == "4":
                appointment_id = int(input("ID запису: "))
                appointment = clinic.complete_appointment(appointment_id)
                print(f"Відвідування позначено: {appointment.status}")

            elif choice == "0":
                print("Роботу завершено.")
                break

            else:
                print("Невідома команда.")

        except ValueError as error:
            print(f"Помилка: {error}")


if __name__ == "__main__":
    main()