import json
import glob


def get_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def change_question_schema(data):
    for i in range(len(data["questions"])):
        if "quest_text" not in data["questions"][i]:
            raise Exception(f"quest_text in {i} not exist")

        old_quest_text = data["questions"][i]["quest_text"]
        question = {
            "main_xpath": old_quest_text["main_xpath"],
            "first_line": old_quest_text["first_line"],
            "second_xpath": old_quest_text["second_xpath"],
            "second_line": old_quest_text["second_line"],
            "is_exact_quest": (
                data["questions"][i]["exact_quest"]
                if "exact_quest" in data["questions"][i]
                else False
            ),
            "missing": (
                old_quest_text["missing"] if "missing" in old_quest_text else None
            ),
            "missing_xp": (
                old_quest_text["missing_xp"] if "missing_xp" in old_quest_text else None
            ),
        }

        del data["questions"][i]["quest_text"]
        if "exact_quest" in data["questions"][i]:
            del data["questions"][i]["exact_quest"]

        data["questions"][i]["question"] = question

    return data


def get_equations(raw_answer):
    equations = []
    for i in range(len(raw_answer) - 2):
        if i == 0:
            continue
        equations.append(raw_answer[i])

    return equations


def change_checkbox_type_schema(data):
    for i in range(len(data["questions"])):
        if data["questions"][i]["format"] != "checkbox":
            continue

        if "answer" not in data["questions"][i]:
            raise Exception(f"answer in {i} not exist")

        old_task = data["questions"][i]
        checkbox_type_answer = {
            "text_chb_xp1": (
                old_task["text_chb_xp1"] if "text_chb_xp1" in old_task else None
            ),
            "text_chb_xp2": (
                old_task["text_chb_xp2"] if "text_chb_xp2" in old_task else None
            ),
            "answer_chb_xp1": (
                old_task["answer_chb_xp1"] if "answer_chb_xp1" in old_task else None
            ),
            "answer_chb_xp2": (
                old_task["answer_chb_xp2"] if "answer_chb_xp2" in old_task else None
            ),
            "is_equations": (
                True if old_task["answer"][0] == "индивидуалочка" else False
            ),
            "equations": (
                get_equations(old_task["answer"])
                if old_task["answer"][0] == "индивидуалочка"
                else None
            ),
            "indices_of_vars": (
                old_task["answer"][-1]
                if old_task["answer"][0] == "индивидуалочка"
                else None
            ),
            "answer_type_var": (
                old_task["type_variable"]
                if old_task["answer"][0] == "индивидуалочка"
                else None
            ),
            "values": (
                None
                if old_task["answer"][0] == "индивидуалочка"
                else old_task["answer"]
            ),
        }

        del data["questions"][i]["answer"]
        if "text_chb_xp1" in data["questions"][i]:
            del data["questions"][i]["text_chb_xp1"]
        if "text_chb_xp2" in data["questions"][i]:
            del data["questions"][i]["text_chb_xp2"]
        if "answer_chb_xp1" in data["questions"][i]:
            del data["questions"][i]["answer_chb_xp1"]
        if "answer_chb_xp2" in data["questions"][i]:
            del data["questions"][i]["answer_chb_xp2"]
        if "type_variable" in data["questions"][i]:
            del data["questions"][i]["type_variable"]

        data["questions"][i]["checkbox_type_answer"] = checkbox_type_answer

    return data


def change_drag_drop_type_schema(data):
    for i in range(len(data["questions"])):
        if data["questions"][i]["format"] != "drag&drop":
            continue

        if "answer" not in data["questions"][i]:
            raise Exception(f"answer in {i} not exist")

        old_task = data["questions"][i]
        drag_drop_type_answer = {
            "array_xp1": (old_task["array_xp1"] if "array_xp1" in old_task else None),
            "array_xp2": (old_task["array_xp2"] if "array_xp2" in old_task else None),
            "array_xp": (old_task["array_xp"] if "array_xp" in old_task else None),
            "answer_xp": (old_task["answer_xp"] if "answer_xp" in old_task else None),
            "array2_xp": (old_task["array2_xp"] if "array2_xp" in old_task else None),
            "multiple_arrays": (
                old_task["multiple_arrays"] if "multiple_arrays" in old_task else 1
            ),
            "values": old_task["answer"],
        }

        del data["questions"][i]["answer"]
        if "array_xp1" in data["questions"][i]:
            del data["questions"][i]["array_xp1"]
        if "array_xp2" in data["questions"][i]:
            del data["questions"][i]["array_xp2"]
        if "array_xp" in data["questions"][i]:
            del data["questions"][i]["array_xp"]
        if "answer_xp" in data["questions"][i]:
            del data["questions"][i]["answer_xp"]
        if "array2_xp" in data["questions"][i]:
            del data["questions"][i]["array2_xp"]
        if "multiple_arrays" in data["questions"][i]:
            del data["questions"][i]["multiple_arrays"]
        if "create_array" in data["questions"][i]:
            del data["questions"][i]["create_array"]

        data["questions"][i]["drag_drop_type_answer"] = drag_drop_type_answer

    return data


def get_bad_parsed_need_exact_value(old_task):
    if "need_exact_value" in old_task:
        if "start" in old_task["need_exact_value"]:
            list = []
            list.append(old_task["need_exact_value"])
            return list
        elif "start" in old_task["need_exact_value"][0]:
            return old_task["need_exact_value"]
        else:
            return None


def change_input_type_schema(data):
    for i in range(len(data["questions"])):
        if data["questions"][i]["format"] != "input":
            continue

        if "answer" not in data["questions"][i]:
            raise Exception(f"answer in {i} not exist")

        old_task = data["questions"][i]
        input_type_answer = {
            "answer_inp_xp": (
                old_task["answer_inp_xp"] if "answer_inp_xp" in old_task else None
            ),
            "string_xpath": (
                old_task["string_xpath"] if "string_xpath" in old_task else None
            ),
            "is_equations": (
                True if old_task["answer"][0] == "индивидуалочка" else False
            ),
            "equations": (
                get_equations(old_task["answer"])
                if old_task["answer"][0] == "индивидуалочка"
                else None
            ),
            "indices_of_vars": (
                old_task["answer"][-1]
                if old_task["answer"][0] == "индивидуалочка"
                else None
            ),
            "answer_type_var": (
                old_task["type_variable"]
                if old_task["answer"][0] == "индивидуалочка"
                else None
            ),
            "need_exact_value": (
                old_task["need_exact_value"]
                if "need_exact_value" in old_task
                and "slice_to" not in old_task["need_exact_value"][0]
                else None
            ),
            "need_exact_value_for_define_var": (
                get_bad_parsed_need_exact_value(old_task)
            ),
            "need_exact_value_with_slice": (
                old_task["need_exact_value"]
                if "need_exact_value" in old_task
                and "slice_to" in old_task["need_exact_value"][0]
                else None
            ),
            "system_of_equations": (
                old_task["system_of_equations"]
                if "system_of_equations" in old_task
                else None
            ),
            "value": (
                None
                if old_task["answer"][0] == "индивидуалочка"
                else old_task["answer"]
            ),
        }

        del data["questions"][i]["answer"]
        if "text_chb_xp1" in data["questions"][i]:
            del data["questions"][i]["text_chb_xp1"]
        if "text_chb_xp2" in data["questions"][i]:
            del data["questions"][i]["text_chb_xp2"]
        if "answer_chb_xp1" in data["questions"][i]:
            del data["questions"][i]["answer_chb_xp1"]
        if "answer_chb_xp2" in data["questions"][i]:
            del data["questions"][i]["answer_chb_xp2"]
        if "type_variable" in data["questions"][i]:
            del data["questions"][i]["type_variable"]

        data["questions"][i]["input_type_answer"] = input_type_answer

    return data


def change_radio_checkbox_type_schema(data):
    for i in range(len(data["questions"])):
        if data["questions"][i]["format"] != "radio checkbox":
            continue

        if "answer" not in data["questions"][i]:
            raise Exception(f"answer in {i} not exist")

        old_task = data["questions"][i]
        radio_checkbox_type_answer = {
            "text_xp1": (old_task["text_xp1"] if "text_xp1" in old_task else None),
            "text_xp2": (old_task["text_xp2"] if "text_xp2" in old_task else None),
            "answer_xp1": (
                old_task["answer_xp1"] if "answer_xp1" in old_task else None
            ),
            "answer_xp2": (
                old_task["answer_xp2"] if "answer_xp2" in old_task else None
            ),
            "value": old_task["answer"],
        }

        del data["questions"][i]["answer"]
        if "text_xp1" in data["questions"][i]:
            del data["questions"][i]["text_xp1"]
        if "text_xp2" in data["questions"][i]:
            del data["questions"][i]["text_xp2"]
        if "answer_xp1" in data["questions"][i]:
            del data["questions"][i]["answer_xp1"]
        if "answer_xp2" in data["questions"][i]:
            del data["questions"][i]["answer_xp2"]

        data["questions"][i]["radio_checkbox_type_answer"] = radio_checkbox_type_answer

    return data


def change_select_type_schema(data):
    for i in range(len(data["questions"])):
        if data["questions"][i]["format"] != "radio checkbox":
            continue

        if "answer" not in data["questions"][i]:
            raise Exception(f"answer in {i} not exist")

        old_task = data["questions"][i]
        select_type_answer = {
            "text_sel_xp1": (
                old_task["text_sel_xp1"] if "text_sel_xp1" in old_task else None
            ),
            "text_sel_xp2": (
                old_task["text_sel_xp2"] if "text_sel_xp2" in old_task else None
            ),
            "answer_sel_xp1": (
                old_task["answer_sel_xp1"] if "answer_sel_xp1" in old_task else None
            ),
            "answer_sel_xp2": (
                old_task["answer_sel_xp2"] if "answer_sel_xp2" in old_task else None
            ),
            "quantity_ans": old_task["quantity_ans"],
            "values": old_task["answer"],
        }

        del data["questions"][i]["answer"]
        if "text_sel_xp1" in data["questions"][i]:
            del data["questions"][i]["text_sel_xp1"]
        if "text_sel_xp2" in data["questions"][i]:
            del data["questions"][i]["text_sel_xp2"]
        if "answer_sel_xp1" in data["questions"][i]:
            del data["questions"][i]["answer_sel_xp1"]
        if "answer_sel_xp2" in data["questions"][i]:
            del data["questions"][i]["answer_sel_xp2"]

        del data["questions"][i]["quantity_ans"]

        data["questions"][i]["select_type_answer"] = select_type_answer

    return data


def change_data_file(data_file):
    data = get_data(data_file)

    try:
        # new_data = change_question_schema(data)
        # new_data = change_checkbox_type_schema(data)
        # new_data = change_drag_drop_type_schema(data)
        # new_data = change_input_type_schema(data)
        # new_data = change_radio_checkbox_type_schema(data)
        new_data = change_select_type_schema(data)
        save_data(data_file, new_data)
        print("data saved for " + data_file)
    except Exception as error:
        print(f"data not saved for {data_file}: {error}")


test_data_file = "assets\\data\\questions_for_2_test.json"
data_filenames = glob.glob("assets\\data\\*.json")

# for data_file in data_filenames:
change_data_file(test_data_file)
