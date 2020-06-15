# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson

import wasp
from apps.snakeNew import SnakeApp
wasp.system.register(SnakeApp())
wasp.system.run()
