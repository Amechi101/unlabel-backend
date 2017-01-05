# -*- coding: utf-8 -*-
def modify_fields(**kwargs):
	def wrap(cls):
		for field, prop_dict in kwargs.items():
			for prop, val in prop_dict.items():
				setattr(cls._meta.get_field(field), prop, val)
		return cls
	return wrap