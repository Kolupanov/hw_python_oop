from typing import Dict, Type, List
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # один шаг
    M_IN_KM: int = 1000  # константа, переводит из м в км
    HOUR_IN_MINUTE: int = 60  # константа, переводит часы в минуты

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Ошибка в расчетах калорий')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18  # первый коэффициет калорий
    COEFF_CALORIE_2: int = 20  # второй коэффициент калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Переопределяем метод количества затраченных калорий."""

        # время тренировки в минутах
        duration_minute = self.duration * self.HOUR_IN_MINUTE
        calories = ((self.COEFF_CALORIE_1
                    * self.get_mean_speed()
                    - self.COEFF_CALORIE_2)
                    * self.weight
                    / self.M_IN_KM
                    * duration_minute)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035  # первый коэффициет калорий
    COEFF_CALORIE_2: float = 0.029  # второй коэффициент калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # принимаем дополнительный параметр - рост

    def get_spent_calories(self) -> float:
        """Переопределяем метод количества затраченных калорий."""

        # время тренировки в минутах
        duration_minute = self.duration * self.HOUR_IN_MINUTE
        calories = ((self.COEFF_CALORIE_1
                    * self.weight
                    + (self.get_mean_speed()**2 // self.height)
                    * self.COEFF_CALORIE_2
                    * self.weight)
                    * duration_minute)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # один гребок
    COEFF_CALORIE_1: float = 1.1  # первый коэффициет калорий
    COEFF_CALORIE_2: float = 2  # второй коэффициент калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        # принимаем дополнительный параметр - длина бассейна
        self.length_pool = length_pool
        # принимаем дополнительный параметр - количество заплывов
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Переопределяем дистанцию"""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Переопределяем метод расчета средней скорости."""
        speed = (self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Переопределяем метод количества затраченных калорий."""
        calories = ((self.get_mean_speed()
                    + self.COEFF_CALORIE_1)
                    * self.COEFF_CALORIE_2
                    * self.weight)
        return calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in workout_types.keys():
        raise KeyError('Передан неверный тип тренировки')
    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
