# encoding: utf-8

# This file is part of CycloneDX Python Lib
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

from unittest import TestCase

from data import get_bom_with_component_setuptools_with_vulnerability

from cyclonedx.model.bom import Bom, ThisTool, Tool
from cyclonedx.model.component import Component, ComponentType


class TestBom(TestCase):

    def test_bom_metadata_tool_this_tool(self) -> None:
        self.assertEqual(ThisTool.vendor, 'CycloneDX')
        self.assertEqual(ThisTool.name, 'cyclonedx-python-lib')
        self.assertNotEqual(ThisTool.version, 'UNKNOWN')

    def test_bom_metadata_tool_multiple_tools(self) -> None:
        bom = Bom()
        self.assertEqual(len(bom.metadata.tools), 1)
        bom.metadata.tools.add(
            Tool(vendor='TestVendor', name='TestTool', version='0.0.0')
        )
        self.assertEqual(len(bom.metadata.tools), 2)

    def test_metadata_component(self) -> None:
        metadata = Bom().metadata
        self.assertTrue(metadata.component is None)
        hextech = Component(name='Hextech', version='1.0.0', component_type=ComponentType.LIBRARY)
        metadata.component = hextech
        self.assertFalse(metadata.component is None)
        self.assertEquals(metadata.component, hextech)

    def test_empty_bom(self) -> None:
        bom = Bom()
        self.assertIsNotNone(bom.uuid)
        self.assertIsNotNone(bom.metadata)
        self.assertFalse(bom.components)
        self.assertFalse(bom.services)
        self.assertFalse(bom.external_references)

    def test_bom_with_vulnerabilities(self) -> None:
        bom = get_bom_with_component_setuptools_with_vulnerability()
        self.assertTrue(bom.has_vulnerabilities())
