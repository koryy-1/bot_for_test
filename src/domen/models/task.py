from pydantic import BaseModel


class Question(BaseModel):
    main_xpath: str
    first_line: str
    second_xpath: str
    second_line: str
    is_exact_quest: str  # используется для парсинга
    missing: str  # также для парсинга
    missing_xp: str


class BaseAnswer(BaseModel):
    pass


class InputTypePlacesForParseValues(BaseModel):
    # TODO: fix this
    var: str | int
    idx: int


class DefinedVarForParse(BaseModel):
    var: int
    start: int
    end: int


class DefinedVarForParseWithSlice(BaseModel):
    var: int
    slice_to: str
    idx: int


class SystemOfEquations(BaseModel):
    var: str
    conditions: list[str]


class SelectTypeItem(BaseModel):
    line: str
    ans: str


class CheckboxTypeAnswer(BaseModel):
    text_chb_xp1: str
    text_chb_xp2: str
    answer_chb_xp1: str
    answer_chb_xp2: str
    is_equations: bool
    equations: list[str]
    indices_of_vars: dict
    answer_type_var: str  # type_variable
    values: list[str]


class DragDropTypeAnswer(BaseModel):
    array_xp1: str
    array_xp2: str
    array_xp: str
    answer_xp: str
    array2_xp: str
    multiple_arrays: int
    values: list[str]


class InputTypeAnswer(BaseModel):
    answer_inp_xp: str
    string_xpath: str
    is_equations: bool
    equations: list[str]
    indices_of_vars: dict
    answer_type_var: str  # type_variable
    # TODO: check json from bot_selenium for need_exact_value schema
    need_exact_value: list[InputTypePlacesForParseValues]
    need_exact_value_for_define_var: list[DefinedVarForParse]
    need_exact_value_with_slice: list[DefinedVarForParseWithSlice]
    system_of_equations: SystemOfEquations
    value: str


class RadioCheckboxTypeAnswer(BaseModel):
    text_xp1: str
    text_xp2: str
    answer_xp1: str
    answer_xp2: str
    value: str


class SelectTypeAnswer(BaseModel):
    text_sel_xp1: str
    text_sel_xp2: str
    answer_sel_xp1: str
    answer_sel_xp2: str
    quantity_ans: int
    # is_exact_answer: bool  # используется для парсинга
    values: list[SelectTypeItem]


# TODO: для каждого типа вопроса (input, select...) сделать классы [type]Answer
# которые наследуются от BaseAnswer
class Task(BaseModel):
    question: Question
    checkbox_type_answer: CheckboxTypeAnswer
    drag_drop_type_answer: DragDropTypeAnswer
    input_type_answer: InputTypeAnswer
    radio_checkbox_type_answer: RadioCheckboxTypeAnswer
    select_type_answer: SelectTypeAnswer
    format: str
