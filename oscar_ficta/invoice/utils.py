class InvoiceNumberGenerator(object):
    """
    Simple object for generating invoice numbers.

    We need this as the invoice number is often required to be
    human editable in case of importing etc
    """

    def invoice_number(self, order_number, invoice_id):
        """
        Return an invoice number for a given order and invoice
        """
        return "%s-%s" % (order_number, invoice_id)