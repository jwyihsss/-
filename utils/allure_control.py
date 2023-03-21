#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import allure
from typing import Any, Dict, Union, Optional


class ReportStyle:
    """allure 报告样式"""

    @staticmethod
    def allure_step(step: str, var: Optional[Union[str, Dict[str, Any]]] = None):
        with allure.step(step):
            allure.attach(
                json.dumps(var, ensure_ascii=False, indent=4),
                step,
                allure.attachment_type.JSON,
            )

    @staticmethod
    def title(title: str):
        allure.dynamic.title(title)

    @staticmethod
    def allure_step_no(step: str):
        """
        无附件的操作步骤
        :param step: 步骤名称
        :return:
        """
        with allure.step(step):
            pass

