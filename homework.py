class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
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
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        coeff_1 = 18
        coeff_2 = 20
        spent_calories: float = ((coeff_1 * self.speed - coeff_2)
                                 * self.weight
                                 / self.M_IN_KM
                                 * (self.duration * 60))
        return spent_calories
    pass


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
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        coeff_1 = 0.035
        coeff_2 = 0.029
        spent_calories = ((coeff_1
                          * self.weight
                          + (self.speed**2 // self.height)
                          * coeff_2
                          * self.weight)
                          * (self.duration * 60))
        return spent_calories
    pass


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.speed: float = 0

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool
                      * self.count_pool
                      / self.M_IN_KM
                      / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        coeff_1: float = 1.1
        coeff_2: float = 2
        spent_calories: float = ((self.get_mean_speed() + coeff_1)
                                 * coeff_2 * self.weight)
        return spent_calories
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    action: int = data[0]
    duration: float = data[1]
    weight: float = data[2]
    if workout_type == 'SWM':
        length_pool: float = data[3]
        count_pool: float = data[4]
        return Swimming(action, duration, weight, length_pool, count_pool)
    elif workout_type == "RUN":
        return Running(action, duration, weight)
    else:
        height: float = data[3]
        return SportsWalking(action, duration, weight, height)


def main(training: Training) -> str:
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
