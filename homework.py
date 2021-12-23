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
        """Создание сообщения."""
        message = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )
        return message


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # метров в км
    MIN_IN_HOUR: int = 60  # минут в часе
    LEN_STEP: float = 0.65  # Длина шага

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
        text_info = InfoMessage(self.__class__.__name__,
                                self.duration,
                                self.get_distance(),
                                self.get_mean_speed(),
                                self.get_spent_calories()
                                )
        return text_info


class Running(Training):
    """Тренировка: бег."""
    COEF_CALORIE_1: float = 18
    COEF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed_calorie = (self.COEF_CALORIE_1
                         * self.get_mean_speed() - self.COEF_CALORIE_2)
        duration_calorie = self.duration * self.MIN_IN_HOUR
        spent_calories = (speed_calorie
                          * self.weight / self.M_IN_KM * duration_calorie)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CALORIE_3 = 0.035
    COEF_CALORIE_4 = 2
    COEF_CALORIE_5 = 0.029

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
        duration_walk = self.duration * self.MIN_IN_HOUR
        weight_1 = self.COEF_CALORIE_3 * self.weight
        weight_2 = self.COEF_CALORIE_5 * self.weight
        speed_height = (self.get_mean_speed()
                        ** self.COEF_CALORIE_4 // self.height)
        calories = (weight_1 + speed_height * weight_2) * duration_walk
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_CALORIE_6 = 1.1
    COEF_CALORIE_7 = 2

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
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.get_mean_speed() + self.COEF_CALORIE_6)
                          * self.COEF_CALORIE_7 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_data = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking
                     }
    if workout_type in training_data:
        workout_dict = training_data[workout_type](*data)
    return workout_dict


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
