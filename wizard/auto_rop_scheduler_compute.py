from odoo import api, models, tools

import logging
import threading

_logger = logging.getLogger(__name__)


class AutoROPSchedulerCompute(models.TransientModel):
    _name = 'auto_rop.scheduler.compute'
    _description = "Run Auto ROP Scheduler Manually"

    def run_scheduler(self):
        with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            cron = self.sudo().env.ref('auto_rop.ir_cron_calculate_rop_action')
            try:
                with tools.mute_logger('odoo.sql_db'):
                    self._cr.execute("SELECT id FROM ir_cron WHERE id = %s FOR UPDATE NOWAIT", (cron.id,))
            except Exception:
                _logger.info("Attempt to run auto rop scheduler aborted, as already running")
                self._cr.rollback()
                self._cr.close()
                return {}

            self.env['stock.warehouse.orderpoint'].run_scheduler(use_new_cursor=self._cr.dbname)

            new_cr.close()
            return {}


    def run_scheduler_manually(self):
        print("Run Scheduler Manually")
        threaded_scheduler = threading.Thread(target=self.run_scheduler, args=())
        threaded_scheduler.start()
        return {'type': 'ir.actions.act_window_close'}