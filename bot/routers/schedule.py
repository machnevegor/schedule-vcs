from aiogram import Router, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from graphs.schedule.searcher import find_schedule
from graphs.student.loader import student_loader
from keyboards.reply.common import quick_keyboard, days_keyboard
from utils.consts import BELL_TIMES

router = Router()


@router.message(F.text == "Звонки")
async def lessons_message(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()

    if not state_data:
        return

    student = await student_loader.load(state_data["student_id"])

    class_number = "8-9" if student.class_number in (8, 9) else "10-11"

    bells = [
        f"{number}. *{time[0]}* – *{time[1]}*"
        for number, time in BELL_TIMES[class_number].items()
    ]

    await message.answer("\n".join(bells))


@router.message(F.text.func(lambda text: text in (
        "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")))
async def lessons_message(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()

    if not state_data:
        return

    schedule = await find_schedule(state_data["student_id"])
    student = await student_loader.load(state_data["student_id"])

    class_number = "8-9" if student.class_number in (8, 9) else "10-11"

    for day in schedule.days:
        if day.name == message.text:
            lessons = [
                f"\[*{BELL_TIMES[class_number][lesson.number][0]}*] {lesson.name}" +
                (f", {lesson.room}" if lesson.room else "")
                for lesson in day.lessons
            ]

            await message.answer(
                "\n".join(lessons),
                reply_markup=quick_keyboard
            )


@router.message(F.text == "Уроки")
async def lessons_message(message: Message) -> None:
    await message.answer(
        "Какой день недели тебя интересует?",
        reply_markup=days_keyboard
    )
