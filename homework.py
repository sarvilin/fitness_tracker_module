from dataclasses import dataclass


@dataclass(frozen=True)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.'
                   )
        return message
    # все значения типа float округляются до 3 знаков после запятой


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # метров в км
    LEN_STEP: float = 0.65
    MIN_HOUR: int = 60

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
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        text_info = InfoMessage(self.__class__.__name__, self.duration,
                                self.get_distance(), self.get_mean_speed(),
                                self.get_spent_calories()
                                )
        return text_info


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: float = 18
    coeff_calorie_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # calc_1 = self.coeff_calorie_1 * self.get_mean_speed() - self.coeff_calorie_2
        # calc_2 = self.weight / self.M_IN_KM * self.duration * self.MIN_HOUR
        # spent_calories = calc_1 * calc_2
        spent_calories = ((self.coeff_calorie_1 * self.get_mean_speed() -
                          self.coeff_calorie_2) * self.weight / self.M_IN_KM *
                         self.duration * self.MIN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calc3 = (
                (0.035 * self.weight + (self.get_mean_speed() ** 2 // self.height) *
                 0.029 * self.weight) * self.duration * self.MIN_HOUR
        )
        calories = calc3
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool /
                     self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_data = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking
                     }
    if workout_type in training_data:
        inini = training_data[workout_type](*data)
    return inini


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
