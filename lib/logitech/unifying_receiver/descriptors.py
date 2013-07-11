#
#
#

from __future__ import absolute_import, division, print_function, unicode_literals

from . import hidpp10 as _hidpp10
from .common import NamedInts as _NamedInts
from .settings_templates import RegisterSettings as _RS, FeatureSettings as _FS

_R = _hidpp10.REGISTERS

#
#
#

from collections import namedtuple
_DeviceDescriptor = namedtuple('_DeviceDescriptor',
				['name', 'kind', 'wpid', 'codename', 'protocol', 'registers', 'settings'])
del namedtuple

DEVICES = {}

def _D(name, codename=None, kind=None, wpid=None, protocol=None, registers=None, settings=None):
	assert name

	if kind is None:
		kind = (_hidpp10.DEVICE_KIND.mouse if 'Mouse' in name
				else _hidpp10.DEVICE_KIND.keyboard if 'Keyboard' in name
				else _hidpp10.DEVICE_KIND.touchpad if 'Touchpad' in name
				else _hidpp10.DEVICE_KIND.trackball if 'Trackball' in name
				else None)
	assert kind is not None, "descriptor for %s does not have 'kind' set" % name

	# heuristic: the codename is the last word in the device name
	if codename is None and ' ' in name:
		codename = name.split(' ')[-1]
	assert codename is not None, "descriptor for %s does not have codename set" % name

	if protocol is not None:
		# ? 2.0 devices should not have any registers
		if protocol < 2.0:
			assert settings is None or all(s._rw.kind == 1 for s in settings)
		else:
			assert registers is None
			assert settings is None or all(s._rw.kind == 2 for s in settings)

	DEVICES[codename] = _DeviceDescriptor(
					name=name,
					kind=kind,
					wpid=wpid,
					codename=codename,
					protocol=protocol,
					registers=registers,
					settings=settings)

	if wpid:
		assert wpid not in DEVICES
		DEVICES[wpid] = DEVICES[codename]

#
#
#

_PERFORMANCE_MX_DPIS = _NamedInts.range(0x81, 0x8F, lambda x: str((x - 0x80) * 100))

#
#
#

# Some HID++1.0 registers and HID++2.0 features can be discovered at run-time,
# so they are not specified here.
#
# For known registers, however, please do specify them here -- avoids
# unnecessary communication with the device and makes it easier to make certain
# decisions when querying the device's state.
#
# Specify a negative value to blacklist a certain register for a device.
#
# Usually, state registers (battery, leds, some features, etc) are only used by
# HID++ 1.0 devices, while HID++ 2.0 devices use features for the same
# functionalities. This is a rule that's been discovered by trial-and-error,
# so it may change in the future.

# Well-known registers (in hex):
#  * 00 - notification flags (all devices)
#    01 - mice: smooth scrolling
#    07 - battery status
#    09 - keyboards: FN swap (if it has the FN key)
#    0D - battery charge
#       a device may have either the 07 or 0D register available;
#       no known device uses both
#    51 - leds
#    63 - mice: DPI
#  * F1 - firmware info
# Some registers appear to be universally supported, no matter the HID++ version
# (marked with *). The rest may or may not be supported, and their values may or
# may not mean the same thing across different devices.

# The 'codename' and 'kind' fields are usually guessed from the device name,
# but in some cases (like the Logitech Cube) that heuristic fails and they have
# to be specified.
#
# The 'protocol' and 'wpid' fields are optional (they can be discovered at
# runtime), but specifying them here speeds up device discovery and reduces the
# USB traffic Solaar has to do to fully identify peripherals.
# Same goes for HID++ 2.0 feature settings (like _feature_fn_swap).
#
# The 'registers' field indicates read-only registers, specifying a state. These
# are valid (AFAIK) only to HID++ 1.0 devices.
# The 'settings' field indicates a read/write register; based on them Solaar
# generates, at runtime, the settings controls in the device panel. HID++ 1.0
# devices may only have register-based settings; HID++ 2.0 devices may only have
# feature-based settings.

# Keyboards

_D('Wireless Keyboard K230', protocol=2.0, wpid='400D')
_D('Wireless Keyboard K270')
_D('Wireless Keyboard K350')
_D('Wireless Keyboard K360', protocol=2.0, wpid='4004',
				settings=[
							_FS.fn_swap()
						],
				)
_D('Wireless Touch Keyboard K400', protocol=2.0, wpid='4024',
				settings=[
							_FS.fn_swap()
						],
				)
_D('Wireless Keyboard MK700', protocol=1.0, wpid='2008',
				registers=(_R.battery_status, ),
				settings=[
							_RS.fn_swap(),
						],
				)
_D('Wireless Solar Keyboard K750', protocol=2.0, wpid='4002',
				settings=[
							_FS.fn_swap()
						],
				)
_D('Wireless Illuminated Keyboard K800', protocol=1.0, wpid='2010',
				registers=(_R.battery_status, _R.three_leds, ),
				settings=[
							_RS.fn_swap(),
						],
				)

# Mice

_D('Wireless Mouse M175', protocol=1.0)
_D('Wireless Mouse M185', protocol=1.0)
_D('Wireless Mouse M187', protocol=1.0)
_D('Wireless Mouse M215', protocol=1.0, wpid='1020')
_D('Wireless Mouse M235', protocol=1.0)
_D('Wireless Mouse M305', protocol=1.0, wpid='101F',
				registers=(_R.battery_status, ),
				)
_D('Wireless Mouse M310', protocol=1.0)
_D('Wireless Mouse M315', protocol=1.0)
_D('Wireless Mouse M317')
_D('Wireless Mouse M325')
_D('Wireless Mouse M345')
_D('Wireless Mouse M505')
_D('Wireless Mouse M510', protocol=1.0, wpid='1025',
				registers=(_R.battery_status, ),
				settings=[
							_RS.smooth_scroll(),
						],
				)
_D('Couch Mouse M515', protocol=2.0)
_D('Wireless Mouse M525', protocol=2.0)
_D('Touch Mouse M600', protocol=2.0, wpid='401A')
_D('Marathon Mouse M705', protocol=1.0, wpid='101B',
				registers=(_R.battery_charge, ),
				settings=[
							_RS.smooth_scroll(),
						],
				)
_D('Zone Touch Mouse T400')
_D('Touch Mouse T620', protocol=2.0)
_D('Logitech Cube', kind=_hidpp10.DEVICE_KIND.mouse, protocol=2.0)
_D('Anywhere Mouse MX', codename='Anywhere MX', protocol=1.0, wpid='1017',
				registers=(_R.battery_charge, ),
				)
_D('Performance Mouse MX', codename='Performance MX', protocol=1.0, wpid='101A',
				registers=(_R.battery_status, _R.three_leds, ),
				settings=[
							_RS.dpi(choices=_PERFORMANCE_MX_DPIS),
						],
				)

# Trackballs

_D('Wireless Trackball M570')

# Touchpads

_D('Wireless Rechargeable Touchpad T650', protocol=2.0)
_D('Wireless Touchpad', codename='Wireless Touch', protocol=2.0, wpid='4011')

#
# Classic Nano peripherals (that don't support the Unifying protocol).
# A wpid is necessary to properly identify them.
#

_D('VX Nano Cordless Laser Mouse', codename='VX Nano', protocol=1.0, wpid='100F',
				registers=(_R.battery_charge, ),
				settings=[
							_RS.smooth_scroll(),
						],
				)
