class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Переопределяем метод количества затраченных калорий."""
        coeff_calorie_1: int = 18  # первый коэффициет калорий
        coeff_calorie_2: int = 20  # второй коэффициент калорий
        # время тренировки в минутах
        duration_minute = self.duration * self.HOUR_IN_MINUTE
        calories = ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                    * self.weight / self.M_IN_KM * duration_minute)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

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
        coeff_calorie_1 = 0.035  # первый коэффициет калорий
        coeff_calorie_2 = 0.029  # второй коэффициент калорий
        # время тренировки в минутах
        duration_minute = self.duration * self.HOUR_IN_MINUTE
        calories = ((coeff_calorie_1
                    * self.weight
                    + (self.get_mean_speed()**2 // self.height)
                    * coeff_calorie_2 * self.weight) * duration_minute)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # один гребок

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
        coeff_calorie_1 = 1.1  # первый коэффициет калорий
        coeff_calorie_2 = 2  # второй коэффициент калорий
        calories = ((self.get_mean_speed()
                    + coeff_calorie_1)
                    * coeff_calorie_2
                    * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    workout = workout_types[workout_type](*data)
    return workout


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
