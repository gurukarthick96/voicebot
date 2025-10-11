from app.ai.llm.prompts.prompt_templates import MENU_AND_USER_INPUT_PROMPT_TEMPLATE


def build_menu_and_user_input_prompt(menu_json: str, user_input: str) -> str:
    return MENU_AND_USER_INPUT_PROMPT_TEMPLATE.format(menu_json=menu_json, user_input=user_input)


__all__ = ['build_menu_and_user_input_prompt']
