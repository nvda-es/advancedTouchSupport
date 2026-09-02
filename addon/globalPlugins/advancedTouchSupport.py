# Advanced Touch Support add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2026 Jose Manuel Delicado <jm.delicado@nvda.es>

import addonHandler
import config
import globalPluginHandler
import wx
import touchTracker
from gui import NVDASettingsDialog, guiHelper
from gui.settingsDialogs import SettingsPanel

addonHandler.initTranslation()

config.conf.spec["touchSupport"] = {
	"minFlickDistance": "integer(default=50)",
}

def applyConfig():
	touchTracker.minFlickDistance = config.conf['touchSupport']['minFlickDistance']

orig_minFlickDistance = touchTracker.minFlickDistance

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()
		config.post_configProfileSwitch.register(self.onConfigChanged)
		config.post_configReset.register(self.onConfigChanged)
		applyConfig()
		NVDASettingsDialog.categoryClasses.append(TouchPanel)

	def terminate(self):
		config.post_configProfileSwitch.unregister(self.onConfigChanged)
		config.post_configReset.unregister(self.onConfigChanged)
		NVDASettingsDialog.categoryClasses.remove(TouchPanel)
		touchTracker.minFlickDistance = orig_minFlickDistance
		super().terminate()

	def onConfigChanged(self, *args, **kwargs):
		applyConfig()


class TouchPanel(SettingsPanel):
	# TRANSLATORS: title for the advanced touch support settings category in NVDA settings dialog
	title = _("Advanced touch support")
	# TRANSLATORS: description for the advanced touch support settings panel
	panelDescription = _(
		"The following options allow you to configure advanced features of your touchscreen so you can work with it in a more comfortable way",
	)

	def makeSettings(self, sizer):
		helper = guiHelper.BoxSizerHelper(self, sizer=sizer)
		helper.addItem(wx.StaticText(self, label=self.panelDescription))
		self.min_flick_distance = helper.addLabeledControl(
			# TRANSLATORS: minimum flick distance on a touch screen
			_("Minimum flick distance (in pixels, default 50): "),
			wx.SpinCtrl,
			min=1,
			max=2000,
			value=str(config.conf['touchSupport']['minFlickDistance']),
		)

	def onSave(self):
		config.conf["touchSupport"]["minFlickDistance"] = self.min_flick_distance.GetValue()
		applyConfig()
