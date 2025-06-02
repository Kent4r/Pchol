import pandas as pd
from datetime import datetime

def process_weather_data(input_file, output_file):
    # Загрузка данных из CSV
    df = pd.read_csv(input_file)
    
    # Преобразование колонки "Дата" в datetime и извлечение месяца и года
    df['Дата'] = pd.to_datetime(df['Дата'], errors='coerce')
    df['Год-Месяц'] = df['Дата'].dt.to_period('M')
    
    # Проверка на случай, если даты не распознались
    if df['Год-Месяц'].isnull().any():
        print("Предупреждение: Некоторые даты не были корректно распознаны.")
    
    # Группировка по месяцу и вычисление агрегатов
    grouped = df.groupby('Год-Месяц').agg({
        'Максимальная температура': 'max',
        'Минимальная температура': 'min',
        'Осадки мм': 'sum'
    })
    
    # Для остальных колонок вычисляем среднее
    other_columns = [col for col in df.columns 
                    if col not in ['Дата', 'Год-Месяц', 'Максимальная температура', 
                                  'Минимальная температура', 'Осадки мм']]
    
    for col in other_columns:
        grouped[col] = df.groupby('Год-Месяц')[col].mean()
    
    # Сброс индекса для удобства (превращаем год-месяц в обычную колонку)
    grouped = grouped.reset_index()
    grouped['Год-Месяц'] = grouped['Год-Месяц'].astype(str)
    
    # Сохранение результатов
    grouped.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Данные успешно обработаны и сохранены в {output_file}")

# Пример использования
if __name__ == "__main__":
    input_csv = "weather.csv"  # Замените на ваш входной файл
    output_csv = "weather_monthly_stats.csv"  # Замените на желаемое имя выходного файла
    
    process_weather_data(input_csv, output_csv)