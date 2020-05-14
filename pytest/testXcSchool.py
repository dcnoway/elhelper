# coding=utf-8
import pytest
from xcschool import xcSchoolSeminars
def testXcSchool():
    s = xcSchoolSeminars()
    assert len(s)>0