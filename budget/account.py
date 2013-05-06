# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Arnaud Wüst
#    Copyright 2009-2013 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm


class account_period(orm.Model):
    """ add new methods to the account_period base object """
    _inherit = 'account.period'

    # XXX context is not propagated from the view,
    # so we never have 'version_id', check if it is a bug
    # or a 'feature'
    def search(self, cr, uid, args, offset=0, limit=None, order=None,
               context=None, count=False):
        """ Special search. If we search a period from the budget
        version form (in the budget lines)  then the choice is reduce to
        periods that overlap the budget dates """
        if context is None:
            context = {}
        period_ids = super(account_period, self).search(
            cr, uid, args, offset, limit, order, context, count)

        # special search limited to a version
        if context.get('version_id'):
            # get version's periods
            version_obj = self.pool.get('budget.version')
            version = version_obj.browse(cr,
                                         uid,
                                         context['version_id'],
                                         context=context)
            allowed_periods = version_obj._get_periods(cr,
                                                       uid,
                                                       version,
                                                       context=context)
            allowed_periods_ids = [p.id for p in allowed_periods]

            # match version's period with parent search result
            period_ids = [period_id for period_id in period_ids
                          if period_id in allowed_periods_ids]
        return period_ids
