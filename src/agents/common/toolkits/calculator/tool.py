"""Calculator tool for basic arithmetic operations."""

import logging

from langchain.tools import tool

logger = logging.getLogger(__name__)


@tool(name_or_callable="calculator", description="可以对给定的 2 个数字选择进行 add, subtract, multiply, divide 运算")
def calculator(a: float, b: float, operation: str) -> float:
    """对两个数字进行基本运算。

    Args:
        a: 第一个数字
        b: 第二个数字
        operation: 运算类型，支持 add, subtract, multiply, divide

    Returns:
        运算结果

    Raises:
        ZeroDivisionError: 当除数为 0 时
        ValueError: 当运算类型不支持时
    """
    try:
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                raise ZeroDivisionError("除数不能为零")
            return a / b
        else:
            raise ValueError(f"不支持的运算类型：{operation}，仅支持 add, subtract, multiply, divide")
    except Exception as e:
        logger.error(f"Calculator error: {e}")
        raise
