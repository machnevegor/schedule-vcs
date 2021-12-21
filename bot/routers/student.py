from aiogram import Router, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from graphs.student.loader import student_loader
from graphs.student.searcher import find_student
from keyboards.inline.common import OptionCallback, PayloadCallback
from keyboards.reply.common import quick_keyboard
from states.common import Auth

router = Router()


@router.callback_query(Auth.full_name, PayloadCallback.filter(F.option == "confirm"))
async def full_name_callback(query: CallbackQuery, state: FSMContext, callback_data: PayloadCallback) -> None:
    await state.update_data(student_id=callback_data.payload)
    await state.set_state(state=None)

    await query.message.edit_text("Приятно познакомиться!")
    await query.message.answer(
        "Ты уже можешь начинать искать своё персональное расписание. "
        "Как тебе, кстати, быстрая клавиатура снизу?)",
        reply_markup=quick_keyboard
    )


@router.callback_query(Auth.full_name, PayloadCallback.filter(F.option == "choose"))
async def full_name_callback(query: CallbackQuery, callback_data: PayloadCallback) -> None:
    student = await student_loader.load(callback_data.payload)

    keyboard = InlineKeyboardBuilder().row(
        InlineKeyboardButton(
            text="Да",
            callback_data=PayloadCallback(
                group="auth",
                state="full_name",
                option="confirm",
                payload=student.id
            ).pack()
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=OptionCallback(
                group="auth",
                state="full_name",
                option="retry"
            ).pack()
        )
    ).as_markup()

    await query.message.edit_text(
        f"То есть ты учишься в {student.class_number} классе "
        f"и это твоё [текущее расписание]({student.table_link})?",
        disable_web_page_preview=True,
        reply_markup=keyboard
    )


@router.callback_query(Auth.full_name, OptionCallback.filter(F.option == "retry"))
async def full_name_callback(query: CallbackQuery) -> None:
    await query.message.edit_text(
        "Странно, очень странно. Может попробовать "
        "как-то по-другому ввести имя и фамилию?"
    )


@router.message(Auth.full_name)
async def full_name_message(message: Message) -> None:
    student_matches = await find_student(message.text)

    if len(student_matches) == 1:
        student = student_matches[0]

        keyboard = InlineKeyboardBuilder().row(
            InlineKeyboardButton(
                text="Да",
                callback_data=PayloadCallback(
                    group="auth",
                    state="full_name",
                    option="confirm",
                    payload=student.id
                ).pack()
            ),
            InlineKeyboardButton(
                text="Нет",
                callback_data=OptionCallback(
                    group="auth",
                    state="full_name",
                    option="retry"
                ).pack()
            )
        ).as_markup()

        await message.answer(
            "Смотри, в базе я нашёл похожую запись с именем "
            f"*{student.first_name} {student.last_name}*, к которой "
            f"привязана [таблица]({student.table_link}). Это ты?",
            disable_web_page_preview=True,
            reply_markup=keyboard
        )

    elif len(student_matches):
        student_buttons = [
            InlineKeyboardButton(
                text=student.first_name + " " + student.last_name,
                callback_data=PayloadCallback(
                    group="auth",
                    state="full_name",
                    option="choose",
                    payload=student.id
                ).pack()
            )
            for student in student_matches
        ]

        keyboard = InlineKeyboardBuilder().row(
            *student_buttons,
            InlineKeyboardButton(
                text="А меня тут нет(",
                callback_data=OptionCallback(
                    group="auth",
                    state="full_name",
                    option="retry"
                ).pack()
            ),
            width=1
        ).as_markup()

        await message.answer(
            "О, я нашёл несколько похожих записей у себя в базе. "
            "Выбери какая из них соответствует твоему имени.",
            reply_markup=keyboard
        )

    else:
        await message.answer(
            "Так-так-так... Что-то я не могу найти похожую "
            "запись в базе. Можешь, пожалуйста, полностью "
            "сказать свои имя и фамилию?"
        )


@router.message(commands="start")
async def start_message(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Привет! У меня нет имени, но ты можешь называть "
        "меня просто ботиком. Думаю, ты уже знаешь, что я "
        "умею искать расписание, и, вполне вероятно, "
        "ты именно за ним."
    )

    await state.set_state(Auth.full_name)
    await message.answer("А тебя как зовут?")
