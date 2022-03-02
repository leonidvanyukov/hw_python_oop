from dataclasses import dataclass

LEN_STEP: float = 0.65
M_IN_KM: float = 1000
MINUTES: float = 60

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration_h: float
    distance_km: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return(self.MESSAGE.format(
            training_type=self.training_type,
            duration=self.duration_h,
            distance=self.distance_km,
            speed=self.speed,
            calories=self.calories
        ))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration_h: float
    weight_kg: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration_h
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_1: float = 18
    COEFF_2: float = 20

    def get_spent_calories(self) -> float:
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        spent_calories: float = ((self.COEFF_1 * self.speed - self.COEFF_2)
                                 * self.weight_kg
                                 / M_IN_KM
                                 * (self.duration_h * MINUTES))
        return spent_calories

@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    COEFF_1 = 0.035
    COEFF_2 = 0.029

    def get_spent_calories(self) -> float:
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        spent_calories = ((self.COEFF_1
                          * self.weight_kg
                          + (self.speed**2 // self.height)
                          * self.COEFF_2
                          * self.weight_kg)
                          * (self.duration_h * MINUTES))
        return spent_calories

@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    LEN_STEP: float = 1.38
    COEFF_1: float = 1.1
    COEFF_2: float = 2

    def get_mean_speed(self) -> float:
        return(self.length_pool
               * self.count_pool
               / M_IN_KM
               / self.duration_h)

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.get_mean_speed() + self.COEFF_1)
                                 * self.COEFF_2 * self.weight_kg)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return(workouts[workout_type](*data))


def main(training: Training) -> None:
    """Главная функция."""
    message = training.show_training_info()
    print(message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
