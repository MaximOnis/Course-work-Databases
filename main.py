import random
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pandas as pd
from datetime import datetime


admin = mysql.connector.connect(
  host="localhost",
  user="root",
  password="maximonis",
  database="store"
)


class Searcher:
    def __init__(self):
        pass

    @staticmethod
    def search_text_having_none(column: str, text: str, result: pd.DataFrame):
        if not text == "":
            if text == "-":
                result = result[(result[column].apply(lambda x: str(x) == "None"))]
            else:
                result = result[(result[column].apply(lambda x: text in str(x)))]
        return result

    @staticmethod
    def search_text_from_list(column: str, text: str, result: pd.DataFrame):
        if not text == "":
            if text == "-":
                result = result[(result[column].apply(lambda x: str(x) == "None"))]
            else:
                result = result[(result[column].apply(lambda x: str(x) == text))]
        return result

    @staticmethod
    def search_diapazone(column: str, from_val: int | float | str, to_val: int | float | str, result: pd.DataFrame, error_mes: str):
        if not (from_val == "" or to_val == ""):
            try:
                from_val = int(from_val)
                to_val = int(to_val)
                if from_val > to_val:
                    messagebox.showwarning("showwarning", error_mes)
                else:
                    result = result[
                        (result[column] >= from_val) & (result[column] <= to_val)]
            except ValueError:
                messagebox.showwarning("showwarning", error_mes)
        return result

    @staticmethod
    def search_date_diapazone(column: str, from_val: str, to_val: str, result: pd.DataFrame, error_mes: str):
        if not (from_val == "" or to_val == ""):
            try:
                from_val = datetime.strptime(from_val, "%Y-%m-%d")
                to_val = datetime.strptime(to_val, "%Y-%m-%d")
                if from_val > to_val:
                    messagebox.showwarning("showwarning", error_mes)
                else:
                    result = result[(result[column].apply(lambda x: datetime.strptime(str(x), "%Y-%m-%d")) >= from_val)
                                    & (result[column].apply(lambda x: datetime.strptime(str(x), "%Y-%m-%d")) <= to_val)]
            except ValueError:
                messagebox.showwarning("showwarning", error_mes)
        return result


class Window:
    def __init__(self):
        self.__win = ctk.CTk()
        self.__win.geometry("1350x550+150+20")
        self.__win.protocol("WM_DELETE_WINDOW", self.on_closing)

        info = ctk.CTkFrame(self.__win)
        info.pack(pady=40, padx=10)

        self.__scroll_y = ttk.Scrollbar(info)
        self.__table = ttk.Treeview(info,
                                    yscrollcommand=self.__scroll_y.set,
                                    height=20,
                                    show='headings')

        self.__scroll_y.config(command=self.__table.yview)

        buttons = ctk.CTkFrame(self.__win)
        buttons.pack(padx=10)

        self.__all = ctk.CTkButton(buttons, text="Вивести список", command=self.all)
        self.__all.grid(column=0, row=0, stick="ew", pady=3, padx=5)

        self.__sort = ctk.CTkButton(buttons, text="Сортувати", command=self.sort)
        self.__sort.grid(column=1, row=0, stick="ew", pady=3, padx=5)

        self.__type_of_sort = ttk.Combobox(buttons,
                                           state="readonly",
                                           foreground="black",
                                           font=("Times new Roman", 13)
                                           )
        self.__type_of_sort.grid(column=1, row=1, stick="ew", pady=3, padx=5)

        self.__docum = ctk.CTkButton(buttons, text="Сформувати звіт", command=self.to_doc)
        self.__docum.grid(column=2, row=0, stick="ew", pady=3, padx=5)

        self.__name_doc = ctk.CTkEntry(buttons,
                                       font=("Times new Roman", 13))
        self.__name_doc.grid(column=2, row=1, stick="ew", pady=3, padx=5)

        self.__delete = ctk.CTkButton(buttons, text="Видалити", command=self.delete_selected_item)
        self.__delete.grid(column=3, row=0, stick="ew", pady=3, padx=5)

        self.__delete_en = ctk.CTkEntry(buttons,
                                        font=("Times new Roman", 13))
        self.__delete_en.grid(column=3, row=1, stick="ew", pady=3, padx=5)

        self.__create = ctk.CTkButton(buttons, text="Додати")
        self.__create.grid(column=4, row=0, stick="ew", pady=3, padx=5)

        self.__edit = ctk.CTkButton(buttons, text="Редагувати", command=self.edit)
        self.__edit.grid(column=5, row=0, stick="ew", pady=3, padx=5)

        self.__edit_en = ctk.CTkEntry(buttons,
                                      font=("Times new Roman", 13))
        self.__edit_en.grid(column=5, row=1, stick="ew", pady=3, padx=5)

        self.__search = ctk.CTkButton(buttons, text="Пошук", command=self.search)
        self.__search.grid(column=6, row=0, stick="ew", pady=3, padx=5)

        self.__cursor = admin.cursor()

    def all(self, dataframe):
        self.clear_table()
        for index, row in dataframe.iterrows():
            values = tuple(row.values)
            self.__table.insert("", tk.END, values=values)

    def search(self):
        return

    def to_doc(self, my_input):
        name = self.__name_doc.get()
        my_input.to_excel(name+".xlsx")
        messagebox.showinfo("showinfo", "Звіт записано")

    def edit(self):
        pass

    def delete_selected_item(self, pageid, page):
        res = self.__delete_en.get()
        try:
            self.__cursor.execute("DELETE FROM "+page+" WHERE "+pageid+" = " + res + ";")
            admin.commit()
        except mysql.connector.errors.ProgrammingError:
            return

    def sort(self):
        pass

    def clear_table(self):
        self.__table.delete(*self.__table.get_children())

    def run(self):
        self.__win.mainloop()

    def on_closing(self):
        try:
            self.__win.destroy()
        except Exception:
            return


# ---------------------------------------------------------------------------------------------------------------
class ProductsWin(Window):
    def __init__(self):
        super().__init__()
        self._Window__type_of_sort["values"] = ("Код продукту", "Виробник", "Ціна", "Дата виготовлення", "Тип",  "Кількість")
        self._Window__win.title("Товари")
        self._Window__table.configure(columns=("Код продукту", "Виробник", "Ціна", "Дата виготовлення", "Тип", "Опис продукту", "Кількість"))
        self._Window__table.heading("Код продукту", text="Код продукту")
        self._Window__table.heading("Виробник", text="Виробник")
        self._Window__table.heading("Ціна", text="Ціна")
        self._Window__table.heading("Дата виготовлення", text="Дата виготовлення")
        self._Window__table.heading("Тип", text="Тип")
        self._Window__table.heading("Опис продукту", text="Опис продукту")
        self._Window__table.heading("Кількість", text="Кількість")
        self._Window__table.pack(side="left")
        self._Window__create.configure(command=self.create)

        self._Window__scroll_y.pack(side="right", fill="y")
        
        self.__result = None

    def all(self, **kwargs):
        self.__result = pd.read_sql("""
            SELECT
            p.ProductID,
            v.name AS VendorName,
            p.price,
            p.ProdDate,
            p.type,
            p.description,
            p.quantity
        FROM
            products p
        LEFT JOIN
            vendors v ON p.vendorID = v.VendorID;""", con=admin)
        super().all(self.__result)

    def search(self):
        search_win = ctk.CTk()
        search_win.title("Пошук")

        top = ctk.CTkLabel(search_win, text="Пошук", font=("Times New Roman", 28))
        top.grid(stick="ew", row=0, columnspan=2, pady=10)

        kod_label = ctk.CTkLabel(search_win, text="Діапазон кодів", font=("Times New Roman", 15))
        kod_label.grid(stick="ew", row=1,  columnspan=2)
        from_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        from_kod.grid(stick="ew", row=2, column=0, padx=3)
        to_kod.grid(stick="ew", row=2, column=1, padx=3)

        vendor_label = ctk.CTkLabel(search_win, text="Назва виробника", font=("Times New Roman", 15))
        vendor_label.grid(stick="ew", row=3, columnspan=2)
        vendor_in = ttk.Combobox(search_win,
                                 state="readonly",
                                 foreground="black",
                                 font=("Times new Roman", 15))
        res = pd.read_sql("SELECT name FROM vendors ORDER BY name", con=admin)
        res = list(res["name"])
        res.insert(0, "")
        vendor_in["values"] = tuple(res)
        vendor_in.grid(stick="ew", row=4, columnspan=2)

        price_label = ctk.CTkLabel(search_win, text="Діапазон цін", font=("Times New Roman", 15))
        price_label.grid(stick="ew", row=5, columnspan=2)
        from_price = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_price = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        from_price.grid(stick="ew", row=6, column=0, padx=3)
        to_price.grid(stick="ew", row=6, column=1, padx=3)

        date_label = ctk.CTkLabel(search_win, text="Діапазон дати(рік-місяць-день)", font=("Times New Roman", 15))
        date_label.grid(stick="ew", row=7, columnspan=2)
        from_date = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_date = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        from_date.grid(stick="ew", row=8, column=0, padx=3)
        to_date.grid(stick="ew", row=8, column=1, padx=3)

        type_label = ctk.CTkLabel(search_win, text="Тип товару", font=("Times New Roman", 15))
        type_label.grid(stick="ew", row=9, columnspan=2)
        type_in = ttk.Combobox(search_win,
                               state="readonly",
                               foreground="black",
                               font=("Times new Roman", 15))
        type_in["values"] = ("", "-", "laptop", "phone", "headphones", "PC")
        type_in.grid(stick="ew", row=10, columnspan=2)

        desc_label = ctk.CTkLabel(search_win, text="Інформація про товар", font=("Times New Roman", 15))
        desc_label.grid(stick="ew", row=11, columnspan=2)
        desc_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        desc_in.grid(stick="ew", row=12, columnspan=2)

        qua_label = ctk.CTkLabel(search_win, text="Діапазон кількості на складі", font=("Times New Roman", 15))
        qua_label.grid(stick="ew", row=13, columnspan=2)
        from_qua = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_qua = ctk.CTkEntry(search_win, font=("Times New Roman", 15))
        from_qua.grid(stick="ew", row=14, column=0)
        to_qua.grid(stick="ew", row=14, column=1)

        def search_g():

            search = Searcher()

            self.__result = pd.read_sql("""
                        SELECT
                        p.ProductID,
                        v.name AS VendorName,
                        p.price,
                        p.ProdDate,
                        p.type,
                        p.description,
                        p.quantity
                    FROM
                        products p
                    LEFT JOIN
                        vendors v ON p.vendorID = v.VendorID;""", con=admin)

            from_id = from_kod.get()
            to_id = to_kod.get()
            self.__result = search.search_diapazone("ProductID", from_id, to_id, self.__result, "Нeправильно вказано діапазон кодів(умову не зараховано)")

            vendor = vendor_in.get()
            self.__result = search.search_text_from_list("VendorName", vendor, self.__result)

            price_from = from_price.get()
            price_to = to_price.get()
            self.__result = search.search_diapazone("price", price_from, price_to, self.__result, "Направильно вказано діапазон цін(умову не зараховано)")

            date_from = from_date.get()
            date_to = to_date.get()
            self.__result = search.search_date_diapazone("ProdDate", date_from, date_to, self.__result, "Направильно вказано діапазон дат(умову не зараховано)")

            type_p = type_in.get()
            self.__result = search.search_text_from_list("type", type_p, self.__result)

            desc = desc_in.get()
            self.__result = search.search_text_having_none("description", desc, self.__result)

            qua_from = from_qua.get()
            qua_to = to_qua.get()
            self.__result = search.search_diapazone("quantity", qua_from, qua_to, self.__result,
                                                    "Направильно вказано діапазон кількості(умову не зараховано)")
            self.clear_table()
            for index, row in self.__result.iterrows():
                values = tuple(row.values)
                self._Window__table.insert("", tk.END, values=values)

        submit = ctk.CTkButton(search_win, text="Знайти", command=search_g)
        submit.grid(stick="ew", row=15, columnspan=2, pady=20, padx=40)

        search_win.mainloop()

    def create(self):
        create_win = ctk.CTk()
        create_win.title("Створення")

        top = ctk.CTkLabel(create_win, text="Створення", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        vendor_label = ctk.CTkLabel(create_win, text="Назва виробника", font=("Times New Roman", 15))
        vendor_label.grid(stick="ew")
        vendor_in = ttk.Combobox(create_win,
                                 state="readonly",
                                 foreground="black",
                                 font=("Times new Roman", 15))
        resq = pd.read_sql("SELECT name FROM vendors ORDER BY name", con=admin)
        resq = list(resq["name"])
        resq.insert(0, "")
        vendor_in["values"] = tuple(resq)
        vendor_in.grid(stick="ew", padx=10)

        price_label = ctk.CTkLabel(create_win, text="Ціна", font=("Times New Roman", 15))
        price_label.grid(stick="ew")
        price_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        price_in.grid(stick="ew", padx=10)

        date_label = ctk.CTkLabel(create_win, text="Дата(рік-місяць-день)", font=("Times New Roman", 15))
        date_label.grid(stick="ew", row=7, columnspan=2)
        date_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        date_in.grid(stick="ew", padx=10)

        type_label = ctk.CTkLabel(create_win, text="Тип товару", font=("Times New Roman", 15))
        type_label.grid(stick="ew")
        type_in = ttk.Combobox(create_win,
                               state="readonly",
                               foreground="black",
                               font=("Times new Roman", 15))
        type_in["values"] = ("", "laptop", "phone", "headphones", "PC")
        type_in.grid(stick="ew", padx=10)

        desc_label = ctk.CTkLabel(create_win, text="Інформація про товар", font=("Times New Roman", 15))
        desc_label.grid(stick="ew")
        desc_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        desc_in.grid(stick="ew", padx=10)

        qua_label = ctk.CTkLabel(create_win, text="Кількость на складі", font=("Times New Roman", 15))
        qua_label.grid(stick="ew")
        qua_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        qua_in.grid(stick="ew", padx=10)

        def add():

            prod_id = random.randint(30, 100000000)
            vendor = vendor_in.get()
            price = price_in.get()
            date = date_in.get()
            type_p = type_in.get()
            desc = desc_in.get()
            qua = qua_in.get()

            list_args = [prod_id]

            if not vendor == "":
                vendo = pd.read_sql("SELECT VendorID FROM vendors WHERE name = '"+vendor+"';", con=admin)
                vendor = vendo["VendorID"].loc[0]
                list_args.append(str(vendor))
            else:
                messagebox.showwarning("Warning", "Не вказано виробника")
                return

            if not price == "":
                try:
                    price = int(price)
                    list_args.append(price)
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно введено ціну")
            else:
                messagebox.showwarning("Warning", "Не вказано ціни")
                return

            if not date == "":
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    list_args.append(str(date))
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно введено дату")
            else:
                messagebox.showwarning("Warning", "Не вказано дати")
                return

            if not type_p == "":
                list_args.append(str(type_p))
            else:
                messagebox.showwarning("Warning", "Не вказано типу")
                return

            if not desc == "":
                list_args.append(str(desc))
            else:
                messagebox.showwarning("Warning", "Не вказано опису")
                return

            if not qua == "":
                try:
                    qua = int(qua)
                    list_args.append(qua)
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно введено кількість")
            else:
                messagebox.showwarning("Warning", "Не вказано кількість")
                return

            list_args = tuple(list_args)

            self._Window__cursor.execute("INSERT INTO products VALUES "+str(list_args)+";")
            admin.commit()

        submit = ctk.CTkButton(create_win, text="Створити", command=add)
        submit.grid(stick="ew", pady=20, padx=40)

        create_win.mainloop()

    def delete_selected_item(self, **kwargs):
        super().delete_selected_item("ProductID", "products")

    def edit(self):
        p_id = self._Window__edit_en.get()
        all_id = pd.read_sql("SELECT ProductID FROM products", con=admin)
        all_id = all_id["ProductID"].tolist()
        try:
            p_id = int(p_id)
        except ValueError:
            messagebox.showwarning("warning", "Неправильно введено код продукту")
            return

        if p_id not in all_id:
            messagebox.showwarning("Warning", "Немає такого продукту")
            return

        edit_win = ctk.CTk()
        edit_win.title("Редагування")

        top = ctk.CTkLabel(edit_win, text="Редагування", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        vendor_label = ctk.CTkLabel(edit_win, text="Назва виробника", font=("Times New Roman", 15))
        vendor_label.grid(stick="ew")
        vendor_in = ttk.Combobox(edit_win,
                                 state="readonly",
                                 foreground="black",
                                 font=("Times new Roman", 15))
        resq = pd.read_sql("SELECT name FROM vendors ORDER BY name", con=admin)
        resq = list(resq["name"])
        resq.insert(0, "")
        vendor_in["values"] = tuple(resq)
        vendor_in.grid(stick="ew", padx=10)

        price_label = ctk.CTkLabel(edit_win, text="Ціна", font=("Times New Roman", 15))
        price_label.grid(stick="ew")
        price_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        price_in.grid(stick="ew", padx=10)

        date_label = ctk.CTkLabel(edit_win, text="Дата(рік-місяць-день)", font=("Times New Roman", 15))
        date_label.grid(stick="ew", row=7, columnspan=2)
        date_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        date_in.grid(stick="ew", padx=10)

        type_label = ctk.CTkLabel(edit_win, text="Тип товару", font=("Times New Roman", 15))
        type_label.grid(stick="ew")
        type_in = ttk.Combobox(edit_win,
                               state="readonly",
                               foreground="black",
                               font=("Times new Roman", 15))
        type_in["values"] = ("", "laptop", "phone", "headphones", "PC")
        type_in.grid(stick="ew", padx=10)

        desc_label = ctk.CTkLabel(edit_win, text="Інформація про товар", font=("Times New Roman", 15))
        desc_label.grid(stick="ew")
        desc_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        desc_in.grid(stick="ew", padx=10)

        qua_label = ctk.CTkLabel(edit_win, text="Кількость на складі", font=("Times New Roman", 15))
        qua_label.grid(stick="ew")
        qua_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        qua_in.grid(stick="ew", padx=10)

        def edit_q():

            vendor = vendor_in.get()
            price = price_in.get()
            date = date_in.get()
            type_p = type_in.get()
            desc = desc_in.get()
            qua = qua_in.get()

            if not vendor == "":
                self._Window__cursor.execute("""
                                            UPDATE products
                                            SET VendorID = (SELECT VendorID
                                                            FROM vendors
                                                            WHERE name = '""" + str(vendor) + """') 
                                            WHERE ProductID = """ + str(p_id) + ";")
                admin.commit()

            if not price == "":
                try:
                    price = int(price)
                    self._Window__cursor.execute("UPDATE products SET price = "+str(price)+" WHERE ProductID = "+str(p_id)+";")
                    admin.commit()
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно введено ціну")

            if not date == "":
                try:
                    self._Window__cursor.execute("UPDATE products SET ProdDate = '"+str(date)+"' WHERE ProductID = "+str(p_id)+";")
                    admin.commit()
                except mysql.connector.errors.DataError:
                    messagebox.showwarning("Warning", "Неправильно введено дату")

            if not desc == "":
                self._Window__cursor.execute("UPDATE products SET description = '"+desc+"' WHERE ProductID = "+str(p_id)+";")
                admin.commit()

            if not qua == "":
                try:
                    qua = int(qua)
                    self._Window__cursor.execute("UPDATE products SET quantity = "+str(qua)+" WHERE ProductID = "+str(p_id)+";")
                    admin.commit()
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно введено кількість")

            if not type_p == "":
                self._Window__cursor.execute("UPDATE products SET type = '"+type_p+"' WHERE ProductID = "+str(p_id)+";")
                admin.commit()

        submit = ctk.CTkButton(edit_win, text="Змінити", command=edit_q)
        submit.grid(stick="ew", pady=20, padx=40)

        edit_win.mainloop()

    def sort(self):
        type_s = self._Window__type_of_sort.get()
        sort_type = None
        match type_s:
            case "Код продукту":
                sort_type = "ProductID"
            case "Виробник":
                sort_type = "VendorName"
            case "Ціна":
                sort_type = "price"
            case "Дата виготовлення":
                sort_type = "ProdDate"
            case "Тип":
                sort_type = "type"
            case "Кількість":
                sort_type = "quantity"
        if sort_type:
            self.__result = pd.read_sql("""
                            SELECT
                            p.ProductID,
                            v.name AS VendorName,
                            p.price,
                            p.ProdDate,
                            p.type,
                            p.description,
                            p.quantity
                        FROM
                            products p
                        LEFT JOIN
                            vendors v ON p.vendorID = v.VendorID
                            ORDER BY """ + sort_type + ";", con=admin)

        self.clear_table()
        for index, row in self.__result.iterrows():
            values = tuple(row.values)
            self._Window__table.insert("", tk.END, values=values)

    def to_doc(self, **kwargs):
        super().to_doc(self.__result)


# ---------------------------------------------------------------------------------------------------------------
class OrdersWin(Window):
    def __init__(self):
        super().__init__()
        self._Window__type_of_sort["values"] = ("Код замовлення", "Покупець", "Продавець", "Товар", "Дата придбання",  "Оплачено")
        self._Window__win.title("Замовлення")
        self._Window__table.configure(columns=("Код замовлення", "Покупець", "Продукт", "Оплачено", "Дата придбання", "Продавець"))
        self._Window__table.heading("Код замовлення", text="Код замовлення")
        self._Window__table.heading("Покупець", text="Покупець")
        self._Window__table.heading("Продукт", text="Продукт")
        self._Window__table.heading("Оплачено", text="Оплачено")
        self._Window__table.heading("Дата придбання", text="Дата придбання")
        self._Window__table.heading("Продавець", text="Продавець")
        self._Window__table.pack(side="left")
        self._Window__create.configure(command=self.create)

        self._Window__scroll_y.pack(side="right", fill="y")
        self.__result = None

    def all(self, **kwargs):
        self.__result = pd.read_sql("""
            SELECT
            o.OrderID,
            c.name AS CustomerName,
            p.description AS ProdDescription,
            o.IsPayed,
            o.OrderDate,
            s.name AS sellerName
            FROM
                orders o
            LEFT JOIN
                customers c ON c.CustomerID = o.CustomerID
            LEFT JOIN
                products p ON p.ProductID = o.ProductID
            LEFT JOIN
                sellers s ON s.sellerID = o.sellerID;""", con=admin)
        super().all(self.__result)

    def search(self):
        search_win = ctk.CTk()
        search_win.title("Пошук")

        top = ctk.CTkLabel(search_win, text="Пошук", font=("Times New Roman", 28))
        top.grid(stick="ew", row=0, columnspan=2, pady=10)

        kod_label = ctk.CTkLabel(search_win, text="Діапазон кодів", font=("Times New Roman", 15))
        kod_label.grid(stick="ew", row=1,  columnspan=2)
        from_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        from_kod.grid(stick="ew", row=2, column=0, padx=3)
        to_kod.grid(stick="ew", row=2, column=1, padx=3)

        customer_label = ctk.CTkLabel(search_win, text="Ім'я покупця", font=("Times New Roman", 15))
        customer_label.grid(stick="ew", row=3, columnspan=2)
        customer_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        customer_in.grid(stick="ew", row=4, columnspan=2)

        product_label = ctk.CTkLabel(search_win, text="Опис товару", font=("Times New Roman", 15))
        product_label.grid(stick="ew", row=5, columnspan=2)
        product_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        product_in.grid(stick="ew", row=6, columnspan=2)

        ispayed_label = ctk.CTkLabel(search_win, text="Чи оплачено", font=("Times New Roman", 15))
        ispayed_label.grid(stick="ew", row=7, columnspan=2)
        ispayed_in = ttk.Combobox(search_win,
                                  state="readonly",
                                  foreground="black",
                                  font=("Times new Roman", 15))
        ispayed_in["values"] = ("", "Так", "Ні")
        ispayed_in.grid(stick="ew", row=8, columnspan=2)

        date_label = ctk.CTkLabel(search_win, text="Діапазон дати(рік-місяць-день)", font=("Times New Roman", 15))
        date_label.grid(stick="ew", row=9, columnspan=2)
        from_date = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_date = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        from_date.grid(stick="ew", row=10, column=0, padx=3)
        to_date.grid(stick="ew", row=10, column=1, padx=3)

        seller_label = ctk.CTkLabel(search_win, text="Ім'я продавця", font=("Times New Roman", 15))
        seller_label.grid(stick="ew", row=11, columnspan=2)
        seller_in = ttk.Combobox(search_win,
                                 state="readonly",
                                 foreground="black",
                                 font=("Times new Roman", 15))
        res = pd.read_sql("SELECT name FROM sellers ORDER BY name", con=admin)
        res = list(res["name"])
        res.insert(0, "")
        res.insert(0, "-")
        seller_in["values"] = tuple(res)
        seller_in.grid(stick="ew", row=12, columnspan=2)

        def search_g():

            search = Searcher()

            self.__result = pd.read_sql("""
                        SELECT
                        o.OrderID,
                        c.name AS CustomerName,
                        p.description AS ProdDescription,
                        o.IsPayed,
                        o.OrderDate,
                        s.name AS sellerName
                        FROM
                            orders o
                        LEFT JOIN
                            customers c ON c.CustomerID = o.CustomerID
                        LEFT JOIN
                            products p ON p.ProductID = o.ProductID
                        LEFT JOIN
                            sellers s ON s.sellerID = o.sellerID;""", con=admin)

            from_id = from_kod.get()
            to_id = to_kod.get()
            self.__result = search.search_date_diapazone("OrderID", from_id, to_id, self.__result,
                                                         "Направильно вказано діапазон кодів(умову не зараховано)")

            customer = customer_in.get()
            self.__result = search.search_text_having_none("CustomerName", customer, self.__result)

            desc = product_in.get()
            self.__result = search.search_text_having_none("ProdDescription", desc, self.__result)

            ispayed = ispayed_in.get()
            if ispayed == "Так":
                self.__result = self.__result[(self.__result["IsPayed"] == 1)]
            elif ispayed == "Ні":
                self.__result = self.__result[(self.__result["IsPayed"] == 0)]

            date_from = from_date.get()
            date_to = to_date.get()
            self.__result = search.search_date_diapazone("OrderDate", date_from, date_to, self.__result, "Неправильно вказано діапазон дат(умову не зараховано)")

            seller = seller_in.get()
            self.__result = search.search_text_having_none("sellerName", seller, self.__result)

            self.clear_table()
            for index, row in self.__result.iterrows():
                values = tuple(row.values)
                self._Window__table.insert("", tk.END, values=values)

        submit = ctk.CTkButton(search_win, text="Знайти", command=search_g)
        submit.grid(stick="ew", row=13, columnspan=2, pady=20, padx=40)

        search_win.mainloop()

    def create(self):
        create_win = ctk.CTk()
        create_win.title("Створення")

        top = ctk.CTkLabel(create_win, text="Створення", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        customer_label = ctk.CTkLabel(create_win, text="Ім'я покупця", font=("Times New Roman", 15))
        customer_label.grid(stick="ew")
        customer_in = ttk.Combobox(create_win,
                                   state="readonly",
                                   foreground="black",
                                   font=("Times new Roman", 15))
        resq = pd.read_sql("SELECT name FROM customers ORDER BY CustomerID", con=admin)
        resq = list(resq["name"])
        resq.insert(0, "")
        customer_in["values"] = tuple(resq)
        customer_in.grid(stick="ew", padx=10)

        prod_label = ctk.CTkLabel(create_win, text="Товар", font=("Times New Roman", 15))
        prod_label.grid(stick="ew")
        prod_in = ttk.Combobox(create_win,
                               state="readonly",
                               foreground="black",
                               font=("Times new Roman", 15))
        resq = pd.read_sql("SELECT description FROM products ORDER BY description", con=admin)
        resq = list(resq["description"])
        resq.insert(0, "")
        prod_in["values"] = resq
        prod_in.grid(stick="ew", padx=10)

        ispayed_label = ctk.CTkLabel(create_win, text="Чи оплачено", font=("Times New Roman", 15))
        ispayed_label.grid(stick="ew")
        ispayed_in = ttk.Combobox(create_win,
                                  state="readonly",
                                  foreground="black",
                                  font=("Times new Roman", 15))
        ispayed_in["values"] = ("", "Так", "Ні")
        ispayed_in.grid(stick="ew", padx=10)

        date_label = ctk.CTkLabel(create_win, text="Дата(рік-місяць-день)", font=("Times New Roman", 15))
        date_label.grid(stick="ew")
        date_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        date_in.grid(stick="ew", padx=10)

        seller_label = ctk.CTkLabel(create_win, text="Ім'я продавця", font=("Times New Roman", 15))
        seller_label.grid(stick="ew")
        seller_in = ttk.Combobox(create_win,
                                 state="readonly",
                                 foreground="black",
                                 font=("Times new Roman", 15))
        res = pd.read_sql("SELECT name FROM sellers ORDER BY name", con=admin)
        res = list(res["name"])
        res.insert(0, "")
        seller_in["values"] = tuple(res)
        seller_in.grid(stick="ew", padx=10)

        def add():

            order_id = random.randint(30, 100000000)
            customer = customer_in.get()
            product = prod_in.get()
            date = date_in.get()
            ispayed = ispayed_in.get()
            seller = seller_in.get()

            list_args = [order_id]

            if not customer == "":
                custome = pd.read_sql("SELECT CustomerID FROM customers WHERE name = '" + str(customer) + "';", con=admin)
                customer = custome["CustomerID"].loc[0]
                list_args.append(str(customer))
            else:
                messagebox.showwarning("Warning", "Не вказано покупця")
                return

            if not product == "":
                produc = pd.read_sql("SELECT ProductID FROM products WHERE description = '" + str(product) + "';", con=admin)
                product = produc["ProductID"].loc[0]
                list_args.append(str(product))
            else:
                messagebox.showwarning("Warning", "Не вказано товару")
                return

            if not ispayed == "":
                if ispayed == "Так":
                    list_args.append(1)
                elif ispayed == "Ні":
                    list_args.append(0)
            else:
                messagebox.showwarning("Warning", "Не вказано оплату")
                return

            if not date == "":
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    list_args.append(str(date))
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно введено дату")
            else:
                messagebox.showwarning("Warning", "Не вказано дати")
                return

            if not seller == "":
                selle = pd.read_sql("SELECT sellerID FROM sellers WHERE name = '" + str(seller) + "';", con=admin)
                seller = selle["sellerID"].loc[0]
                list_args.append(str(seller))
            else:
                messagebox.showwarning("Warning", "Не вказано продавця")
                return

            list_args = tuple(list_args)

            self._Window__cursor.execute("INSERT INTO orders VALUES " + str(list_args) + ";")
            admin.commit()

        submit = ctk.CTkButton(create_win, text="Створити", command=add)
        submit.grid(stick="ew", pady=20, padx=40)

        create_win.mainloop()

    def delete_selected_item(self, **kwargs):
        super().delete_selected_item("OrderID", "orders")

    def edit(self):
        p_id = self._Window__edit_en.get()
        all_id = pd.read_sql("SELECT OrderID FROM orders", con=admin)
        all_id = all_id["OrderID"].tolist()
        try:
            p_id = int(p_id)
        except ValueError:
            messagebox.showwarning("warning", "Неправильно введено код замовлення")
            return

        if p_id not in all_id:
            messagebox.showwarning("Warning", "Немає такого замовлення")
            return

        edit_win = ctk.CTk()
        edit_win.title("Редагування")

        top = ctk.CTkLabel(edit_win, text="Редагування", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        customer_label = ctk.CTkLabel(edit_win, text="Ім'я покупця", font=("Times New Roman", 15))
        customer_label.grid(stick="ew")
        customer_in = ttk.Combobox(edit_win,
                                   state="readonly",
                                   foreground="black",
                                   font=("Times new Roman", 15))
        resq = pd.read_sql("SELECT name FROM customers ORDER BY CustomerID", con=admin)
        resq = list(resq["name"])
        resq.insert(0, "")
        customer_in["values"] = tuple(resq)
        customer_in.grid(stick="ew", padx=10)

        prod_label = ctk.CTkLabel(edit_win, text="Товар", font=("Times New Roman", 15))
        prod_label.grid(stick="ew")
        prod_in = ttk.Combobox(edit_win,
                               state="readonly",
                               foreground="black",
                               font=("Times new Roman", 15))
        resq = pd.read_sql("SELECT description FROM products ORDER BY description", con=admin)
        resq = list(resq["description"])
        resq.insert(0, "")
        prod_in["values"] = resq
        prod_in.grid(stick="ew", padx=10)

        ispayed_label = ctk.CTkLabel(edit_win, text="Чи оплачено", font=("Times New Roman", 15))
        ispayed_label.grid(stick="ew")
        ispayed_in = ttk.Combobox(edit_win,
                                  state="readonly",
                                  foreground="black",
                                  font=("Times new Roman", 15))
        ispayed_in["values"] = ("", "Так", "Ні")
        ispayed_in.grid(stick="ew", padx=10)

        date_label = ctk.CTkLabel(edit_win, text="Дата(рік-місяць-день)", font=("Times New Roman", 15))
        date_label.grid(stick="ew")
        date_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        date_in.grid(stick="ew", padx=10)

        seller_label = ctk.CTkLabel(edit_win, text="Ім'я продавця", font=("Times New Roman", 15))
        seller_label.grid(stick="ew")
        seller_in = ttk.Combobox(edit_win,
                                 state="readonly",
                                 foreground="black",
                                 font=("Times new Roman", 15))
        res = pd.read_sql("SELECT name FROM sellers ORDER BY name", con=admin)
        res = list(res["name"])
        res.insert(0, "")
        seller_in["values"] = tuple(res)
        seller_in.grid(stick="ew", padx=10)

        def edit_q():

            customer = customer_in.get()
            prod = prod_in.get()
            date = date_in.get()
            ispayed = ispayed_in.get()
            seller = seller_in.get()

            if not customer == "":
                self._Window__cursor.execute("""
                                            UPDATE orders
                                            SET CustomerID = (SELECT CustomerID
                                                            FROM customers
                                                            WHERE name = '""" + str(customer) + """') 
                                            WHERE OrderID = """ + str(p_id) + ";")
                admin.commit()

            if not prod == "":
                self._Window__cursor.execute("""
                                            UPDATE orders
                                            SET ProductID = (SELECT ProductID
                                                            FROM products
                                                            WHERE description = '""" + str(prod) + """') 
                                            WHERE OrderID = """ + str(p_id) + ";")
                admin.commit()

            if not date == "":
                try:
                    self._Window__cursor.execute(
                        "UPDATE orders SET OrderDate = '" + str(date) + "' WHERE OrderID = " + str(p_id) + ";")
                    admin.commit()
                except mysql.connector.errors.DataError:
                    messagebox.showwarning("Warning", "Неправильно введено дату")

            if not ispayed == "":
                if ispayed == "Так":
                    self._Window__cursor.execute("UPDATE orders SET IsPayed = 1 WHERE OrderID = "+str(p_id)+";")
                elif ispayed == "Ні":
                    self._Window__cursor.execute("UPDATE orders SET IsPayed = 0 WHERE OrderID = " + str(p_id) + ";")

            if not seller == "":
                self._Window__cursor.execute("""
                                            UPDATE orders
                                            SET sellerID = (SELECT sellerID
                                                            FROM sellers
                                                            WHERE name = '""" + str(seller) + """') 
                                            WHERE OrderID = """ + str(p_id) + ";")
                admin.commit()

        submit = ctk.CTkButton(edit_win, text="Змінити", command=edit_q)
        submit.grid(stick="ew", pady=20, padx=40)

        edit_win.mainloop()

    def sort(self):
        type_s = self._Window__type_of_sort.get()
        sort_type = None
        match type_s:
            case "Код замовлення":
                sort_type = "OrderID"
            case "Покупець":
                sort_type = "CustomerName"
            case "Продавець":
                sort_type = "sellerName"
            case "Товар":
                sort_type = "ProdDescription"
            case "Дата придбання":
                sort_type = "type"
            case "Оплачено":
                sort_type = "IsPayed"
        if sort_type:
            self.__result = pd.read_sql("""
                                    SELECT
                                    o.OrderID,
                                    c.name AS CustomerName,
                                    p.description AS ProdDescription,
                                    o.IsPayed,
                                    o.OrderDate,
                                    s.name AS sellerName
                                    FROM
                                        orders o
                                    LEFT JOIN
                                        customers c ON c.CustomerID = o.CustomerID
                                    LEFT JOIN
                                        products p ON p.ProductID = o.ProductID
                                    LEFT JOIN
                                        sellers s ON s.sellerID = o.sellerID
                                    ORDER BY""" + sort_type + ";", con=admin)

            self.clear_table()
            for index, row in self.__result.iterrows():
                values = tuple(row.values)
                self._Window__table.insert("", tk.END, values=values)

    def to_doc(self, **kwargs):
        super().to_doc(self.__result)


# ---------------------------------------------------------------------------------------------------------------
class VendorsWin(Window):
    def __init__(self):
        super().__init__()
        self._Window__type_of_sort["values"] = ("Код виробника", "Назва", "Адрес", "Пошта")
        self._Window__win.title("Виробники")
        self._Window__table.configure(columns=("Код виробника", "Назва", "Адрес", "Номер телефону", "Пошта"))
        self._Window__table.heading("Код виробника", text="Код виробника")
        self._Window__table.heading("Назва", text="Назва")
        self._Window__table.heading("Адрес", text="Адрес")
        self._Window__table.heading("Номер телефону", text="Номер телефону")
        self._Window__table.heading("Пошта", text="Пошта")
        self._Window__table.pack(side="left")
        self._Window__create.configure(command=self.create)

        self._Window__scroll_y.pack(side="right", fill="y")
        self.__result = None

    def all(self, **kwargs):
        self.__result = pd.read_sql("""
            SELECT *
            FROM vendors;""", con=admin)
        super().all(self.__result)

    def search(self):
        search_win = ctk.CTk()
        search_win.title("Пошук")

        top = ctk.CTkLabel(search_win, text="Пошук", font=("Times New Roman", 28))
        top.grid(stick="ew", row=0, columnspan=2, pady=10)

        kod_label = ctk.CTkLabel(search_win, text="Діапазон кодів", font=("Times New Roman", 15))
        kod_label.grid(stick="ew", row=1,  columnspan=2)
        from_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        from_kod.grid(stick="ew", row=2, column=0, padx=3)
        to_kod.grid(stick="ew", row=2, column=1, padx=3)

        name_label = ctk.CTkLabel(search_win, text="Назва компанії", font=("Times New Roman", 15))
        name_label.grid(stick="ew", row=3, columnspan=2)
        name_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        name_in.grid(stick="ew", row=4, columnspan=2)

        adress_label = ctk.CTkLabel(search_win, text="Адрес", font=("Times New Roman", 15))
        adress_label.grid(stick="ew", row=5, columnspan=2)
        adress_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        adress_in.grid(stick="ew", row=6, columnspan=2)

        phone_label = ctk.CTkLabel(search_win, text="Номер телефону", font=("Times New Roman", 15))
        phone_label.grid(stick="ew", row=7, columnspan=2)
        phone_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        phone_in.grid(stick="ew", row=8, columnspan=2)

        email_label = ctk.CTkLabel(search_win, text="Пошта", font=("Times New Roman", 15))
        email_label.grid(stick="ew", row=9, columnspan=2)
        email_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        email_in.grid(stick="ew", row=10, columnspan=2)

        def search_g():

            search = Searcher()

            self.__result = pd.read_sql("""
                        SELECT *
                        FROM vendors;""", con=admin)

            from_id = from_kod.get()
            to_id = to_kod.get()
            self.__result = search.search_diapazone("VendorID", from_id, to_id, self.__result, "Направильно вказано діапазон кодів(умову не зараховано)")

            name = name_in.get()
            self.__result = search.search_text_having_none("name", name, self.__result)

            adress = adress_in.get()
            self.__result = search.search_text_having_none("adress", adress, self.__result)

            phone = phone_in.get()
            self.__result = search.search_text_having_none("phoneNumber", phone, self.__result)

            email = email_in.get()
            self.__result = search.search_text_having_none("email", email, self.__result)

            self.clear_table()
            for index, row in self.__result.iterrows():
                values = tuple(row.values)
                self._Window__table.insert("", tk.END, values=values)

        submit = ctk.CTkButton(search_win, text="Знайти", command=search_g)
        submit.grid(stick="ew", row=11, columnspan=2, pady=20, padx=40)

        search_win.mainloop()

    def create(self):
        create_win = ctk.CTk()
        create_win.title("Створення")

        top = ctk.CTkLabel(create_win, text="Створення", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        name_label = ctk.CTkLabel(create_win, text="Назва виробника", font=("Times New Roman", 15))
        name_label.grid(stick="ew")
        name_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        name_in.grid(stick="ew", padx=10)

        adress_label = ctk.CTkLabel(create_win, text="Адрес", font=("Times New Roman", 15))
        adress_label.grid(stick="ew")
        adress_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        adress_in.grid(stick="ew", padx=10)

        phone_label = ctk.CTkLabel(create_win, text="Номер телефону", font=("Times New Roman", 15))
        phone_label.grid(stick="ew")
        phone_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        phone_in.grid(stick="ew", padx=10)

        email_label = ctk.CTkLabel(create_win, text="Пошта", font=("Times New Roman", 15))
        email_label.grid(stick="ew")
        email_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        email_in.grid(stick="ew", padx=10)

        def add():

            ven_id = random.randint(30, 100000000)
            name = name_in.get()
            adress = adress_in.get()
            phone = phone_in.get()
            email = email_in.get()

            list_args = [ven_id]

            if not name == "":
                list_args.append(str(name))
            else:
                messagebox.showwarning("Warning", "Не вказано назви")
                return

            if not adress == "":
                list_args.append(str(adress))
            else:
                messagebox.showwarning("Warning", "Не вказано адреси")
                return

            if not phone == "":
                try:
                    int(phone)
                    list_args.append(str(phone))
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно вказано номер телефону")
                    return
            else:
                messagebox.showwarning("Warning", "Не вказано номеру телефону")
                return

            if not email == "":
                list_args.append(str(email))
            else:
                messagebox.showwarning("Warning", "Не вказано пошти")
                return

            list_args = tuple(list_args)

            self._Window__cursor.execute("INSERT INTO vendors VALUES " + str(list_args) + ";")
            admin.commit()

        submit = ctk.CTkButton(create_win, text="Створити", command=add)
        submit.grid(stick="ew", pady=20, padx=40)

        create_win.mainloop()

    def delete_selected_item(self, **kwargs):
        try:
            super().delete_selected_item("VendorID", "vendors")
        except Exception as e:
            if str(e) == "1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`store`.`products`, CONSTRAINT `fk_vendor` FOREIGN KEY (`VendorID`) REFERENCES `vendors` (`VendorID`))":
                messagebox.showwarning("showwarning", "Даний виробник застосований у іншій таблиці")

    def edit(self):
        p_id = self._Window__edit_en.get()
        all_id = pd.read_sql("SELECT VendorID FROM vendors", con=admin)
        all_id = all_id["VendorID"].tolist()
        try:
            p_id = int(p_id)
        except ValueError:
            messagebox.showwarning("warning", "Неправильно введено код виробника")
            return

        if p_id not in all_id:
            messagebox.showwarning("Warning", "Немає такого виробника")
            return

        edit_win = ctk.CTk()
        edit_win.title("Редагування")

        top = ctk.CTkLabel(edit_win, text="Редагування", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        name_label = ctk.CTkLabel(edit_win, text="Назва виробника", font=("Times New Roman", 15))
        name_label.grid(stick="ew")
        name_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        name_in.grid(stick="ew", padx=10)

        adress_label = ctk.CTkLabel(edit_win, text="Адрес", font=("Times New Roman", 15))
        adress_label.grid(stick="ew", padx=10)
        adress_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        adress_in.grid(stick="ew", padx=10)

        phone_label = ctk.CTkLabel(edit_win, text="Номер телефону", font=("Times New Roman", 15))
        phone_label.grid(stick="ew", padx=10)
        phone_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        phone_in.grid(stick="ew", padx=10)

        email_label = ctk.CTkLabel(edit_win, text="Пошта", font=("Times New Roman", 15))
        email_label.grid(stick="ew")
        email_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        email_in.grid(stick="ew", padx=10)

        def edit_q():

            name = name_in.get()
            adress = adress_in.get()
            phone = phone_in.get()
            email = email_in.get()

            if not name == "":
                self._Window__cursor.execute("UPDATE vendors SET name = '" + str(name) + "' WHERE VendorID = " + str(p_id) + ";")
                admin.commit()

            if not adress == "":
                self._Window__cursor.execute(
                    "UPDATE vendors SET adress = '" + str(adress) + "' WHERE VendorID = " + str(p_id) + ";")
                admin.commit()

            try:
                phone = int(phone)
                if not phone == "":
                    self._Window__cursor.execute("UPDATE vendors SET phoneNumber = '" + str(phone) + "' WHERE VendorID = " + str(p_id) + ";")
                    admin.commit()
            except ValueError:
                messagebox.showwarning("Warning", "Неправильно введено номер")

            if not email == "":
                self._Window__cursor.execute("UPDATE vendors SET email = '" + str(email) + "' WHERE VendorID = " + str(p_id) + ";")
                admin.commit()

        submit = ctk.CTkButton(edit_win, text="Змінити", command=edit_q)
        submit.grid(stick="ew", pady=20, padx=40)

        edit_win.mainloop()

    def sort(self):
        type_s = self._Window__type_of_sort.get()
        sort_type = None
        match type_s:
            case "Код виробника":
                sort_type = "VendorID"
            case "Назва":
                sort_type = "name"
            case "Адрес":
                sort_type = "adress"
            case "Пошта":
                sort_type = "email"
        if sort_type:
            self.__result = pd.read_sql("""
                                    SELECT *
                                    FROM vendors 
                                    ORDER BY """ + sort_type + ";", con=admin)

            self.clear_table()
            for index, row in self.__result.iterrows():
                values = tuple(row.values)
                self._Window__table.insert("", tk.END, values=values)

    def to_doc(self, **kwargs):
        super().to_doc(self.__result)


# ---------------------------------------------------------------------------------------------------------------
class CustomersWin(Window):
    def __init__(self):
        super().__init__()
        self._Window__type_of_sort["values"] = ("Код покупця", "Ім'я", "Прізвище", "По-батькові")
        self._Window__win.title("Покупці")
        self._Window__table.configure(columns=("Код покупця", "Ім'я", "Прізвище", "По-батькові"))
        self._Window__table.heading("Код покупця", text="Код покупця")
        self._Window__table.heading("Ім'я", text="Ім'я")
        self._Window__table.heading("Прізвище", text="Прізвище")
        self._Window__table.heading("По-батькові", text="По-батькові")
        self._Window__table.pack(side="left")
        self._Window__create.configure(command=self.create)

        self._Window__scroll_y.pack(side="right", fill="y")
        self.__result = None

    def all(self, **kwargs):
        self.__result = pd.read_sql("""
            SELECT *
            FROM customers;""", con=admin)
        super().all(self.__result)

    def search(self):

        search_win = ctk.CTk()
        search_win.title("Пошук")

        top = ctk.CTkLabel(search_win, text="Пошук", font=("Times New Roman", 28))
        top.grid(stick="ew", row=0, columnspan=2, pady=10)

        kod_label = ctk.CTkLabel(search_win, text="Діапазон кодів", font=("Times New Roman", 15))
        kod_label.grid(stick="ew", row=1,  columnspan=2)
        from_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        from_kod.grid(stick="ew", row=2, column=0, padx=3)
        to_kod.grid(stick="ew", row=2, column=1, padx=3)

        name_label = ctk.CTkLabel(search_win, text="Ім'я покупця", font=("Times New Roman", 15))
        name_label.grid(stick="ew", row=3, columnspan=2)
        name_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        name_in.grid(stick="ew", row=4, columnspan=2)

        surname_label = ctk.CTkLabel(search_win, text="Прізвище покупця", font=("Times New Roman", 15))
        surname_label.grid(stick="ew", row=5, columnspan=2)
        surname_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        surname_in.grid(stick="ew", row=6, columnspan=2)

        lastname_label = ctk.CTkLabel(search_win, text="По-батькові", font=("Times New Roman", 15))
        lastname_label.grid(stick="ew", row=7, columnspan=2)
        lastname_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        lastname_in.grid(stick="ew", row=8, columnspan=2)

        def search_g():

            search = Searcher()

            self.__result = pd.read_sql("""
                        SELECT *
                        FROM customers;""", con=admin)

            from_id = from_kod.get()
            to_id = to_kod.get()
            self.__result = search.search_diapazone("CustomerID", from_id, to_id, self.__result,
                                                    "Направильно вказано діапазон кодів(умову не зараховано)")

            name = name_in.get()
            self.__result = search.search_text_having_none("name", name, self.__result)

            surname = surname_in.get()
            self.__result = search.search_text_having_none("surname", surname, self.__result)

            lastname = lastname_in.get()
            self.__result = search.search_text_having_none("lastName", lastname, self.__result)

            self.clear_table()
            for index, row in self.__result.iterrows():
                values = tuple(row.values)
                self._Window__table.insert("", tk.END, values=values)

        submit = ctk.CTkButton(search_win, text="Знайти", command=search_g)
        submit.grid(stick="ew", row=9, columnspan=2, pady=20, padx=40)

        search_win.mainloop()

    def create(self):
        create_win = ctk.CTk()
        create_win.title("Створення")

        top = ctk.CTkLabel(create_win, text="Створення", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        name_label = ctk.CTkLabel(create_win, text="Ім'я покупця", font=("Times New Roman", 15))
        name_label.grid(stick="ew")
        name_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        name_in.grid(stick="ew", padx=10)

        surname_label = ctk.CTkLabel(create_win, text="Прізвище покупця", font=("Times New Roman", 15))
        surname_label.grid(stick="ew")
        surname_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        surname_in.grid(stick="ew", padx=10)

        lastname_label = ctk.CTkLabel(create_win, text="По-батькові покупця", font=("Times New Roman", 15))
        lastname_label.grid(stick="ew")
        lastname_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        lastname_in.grid(stick="ew", padx=10)

        def add():

            cus_id = random.randint(30, 100000000)
            name = name_in.get()
            surname = surname_in.get()
            lastname = lastname_in.get()

            list_args = [cus_id]

            if not name == "":
                list_args.append(str(name))
            else:
                messagebox.showwarning("Warning", "Не вказано імені")
                return

            if not surname == "":
                list_args.append(str(surname))
            else:
                messagebox.showwarning("Warning", "Не вказано прізвища")
                return

            if not lastname == "":
                list_args.append(str(lastname))
            else:
                messagebox.showwarning("Warning", "Не вказано по-батькові")
                return

            list_args = tuple(list_args)

            self._Window__cursor.execute("INSERT INTO customers VALUES " + str(list_args) + ";")
            admin.commit()

        submit = ctk.CTkButton(create_win, text="Створити", command=add)
        submit.grid(stick="ew", pady=20, padx=40)

        create_win.mainloop()

    def delete_selected_item(self, **kwargs):
        try:
            super().delete_selected_item("CustomerID", "customers")
        except Exception as e:
            if str(e) == "1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`store`.`orders`, CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`))":
                messagebox.showwarning("showwarning", "Даний покупець застосований у іншій таблиці")

    def edit(self):
        p_id = self._Window__edit_en.get()
        all_id = pd.read_sql("SELECT CustomerID FROM customers", con=admin)
        all_id = all_id["CustomerID"].tolist()
        try:
            p_id = int(p_id)
        except ValueError:
            messagebox.showwarning("warning", "Неправильно введено код покупця")
            return

        if p_id not in all_id:
            messagebox.showwarning("Warning", "Немає такого покупця")
            return

        edit_win = ctk.CTk()
        edit_win.title("Редагування")

        top = ctk.CTkLabel(edit_win, text="Редагування", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        name_label = ctk.CTkLabel(edit_win, text="Ім'я покупця", font=("Times New Roman", 15))
        name_label.grid(stick="ew")
        name_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        name_in.grid(stick="ew", padx=10)

        surname_label = ctk.CTkLabel(edit_win, text="Прізвище покупця", font=("Times New Roman", 15))
        surname_label.grid(stick="ew")
        surname_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        surname_in.grid(stick="ew", padx=10)

        lastname_label = ctk.CTkLabel(edit_win, text="По-батькові покупця", font=("Times New Roman", 15))
        lastname_label.grid(stick="ew")
        lastname_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        lastname_in.grid(stick="ew", padx=10)

        def edit_q():

            name = name_in.get()
            surname = surname_in.get()
            lastname = lastname_in.get()

            if not name == "":
                self._Window__cursor.execute(
                    "UPDATE customers SET name = '" + str(name) + "' WHERE CustomerID = " + str(p_id) + ";")
                admin.commit()

            if not surname == "":
                self._Window__cursor.execute(
                    "UPDATE customers SET surname = '" + str(surname) + "' WHERE CustomerID = " + str(p_id) + ";")
                admin.commit()

            if not lastname == "":
                self._Window__cursor.execute(
                    "UPDATE customers SET lastName = '" + str(lastname) + "' WHERE CustomerID = " + str(p_id) + ";")
                admin.commit()

        submit = ctk.CTkButton(edit_win, text="Змінити", command=edit_q)
        submit.grid(stick="ew", pady=20, padx=40)

        edit_win.mainloop()

    def sort(self):
        type_s = self._Window__type_of_sort.get()
        sort_type = None
        match type_s:
            case "Код виробника":
                sort_type = "CustomerID"
            case "Ім'я":
                sort_type = "name"
            case "Прізвище":
                sort_type = "surname"
            case "По-батькові":
                sort_type = "lastName"
        if sort_type:
            self.__result = pd.read_sql("""
                                    SELECT *
                                    FROM customers 
                                    ORDER BY """ + sort_type + ";", con=admin)

            self.clear_table()
            for index, row in self.__result.iterrows():
                values = tuple(row.values)
                self._Window__table.insert("", tk.END, values=values)

    def to_doc(self, **kwargs):
        self.__result = super().to_doc(self.__result)


# ---------------------------------------------------------------------------------------------------------------
class SellersWin(Window):
    def __init__(self):
        super().__init__()
        self._Window__win.title("Продавці")
        self._Window__type_of_sort["values"] = ("Код продавця", "Ім'я", "Прізвище", "Зарплата")
        self._Window__table.configure(columns=("Код продавця", "Ім'я", "Прізвище", "Зарплата", "Номер телефону"))
        self._Window__table.heading("Код продавця", text="Код продавця")
        self._Window__table.heading("Ім'я", text="Ім'я")
        self._Window__table.heading("Прізвище", text="Прізвище")
        self._Window__table.heading("Зарплата", text="Зарплата")
        self._Window__table.heading("Номер телефону", text="Номер телефону")
        self._Window__table.pack(side="left")
        self._Window__create.configure(command=self.create)

        self._Window__scroll_y.pack(side="right", fill="y")
        self.__result = None

    def all(self, **kwargs):
        self.__result = pd.read_sql("""
            SELECT *
            FROM sellers;""", con=admin)
        super().all(self.__result)

    def search(self):
        search_win = ctk.CTk()
        search_win.title("Пошук")

        top = ctk.CTkLabel(search_win, text="Пошук", font=("Times New Roman", 28))
        top.grid(stick="ew", row=0, columnspan=2, pady=10)

        kod_label = ctk.CTkLabel(search_win, text="Діапазон кодів", font=("Times New Roman", 15))
        kod_label.grid(stick="ew", row=1,  columnspan=2)
        from_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_kod = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        from_kod.grid(stick="ew", row=2, column=0, padx=3)
        to_kod.grid(stick="ew", row=2, column=1, padx=3)

        name_label = ctk.CTkLabel(search_win, text="Ім'я продавця", font=("Times New Roman", 15))
        name_label.grid(stick="ew", row=3, columnspan=2)
        name_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        name_in.grid(stick="ew", row=4, columnspan=2)

        surname_label = ctk.CTkLabel(search_win, text="Прізвище продавця", font=("Times New Roman", 15))
        surname_label.grid(stick="ew", row=5, columnspan=2)
        surname_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        surname_in.grid(stick="ew", row=6, columnspan=2)

        salary_label = ctk.CTkLabel(search_win, text="Діапазон зарплати", font=("Times New Roman", 15))
        salary_label.grid(stick="ew", row=7, columnspan=2)
        from_salary = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        to_salary = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        from_salary.grid(stick="ew", row=8, column=0, padx=3)
        to_salary.grid(stick="ew", row=8, column=1, padx=3)

        phone_label = ctk.CTkLabel(search_win, text="Номер телефону", font=("Times New Roman", 15))
        phone_label.grid(stick="ew", row=9, columnspan=2)
        phone_in = ctk.CTkEntry(search_win, font=("Times new Roman", 15))
        phone_in.grid(stick="ew", row=10, columnspan=2)

        def search_g():

            search = Searcher()

            self.__result = pd.read_sql("""
                        SELECT *
                        FROM sellers;""", con=admin)

            from_id = from_kod.get()
            to_id = to_kod.get()
            self.__result = search.search_diapazone("sellerID", from_id, to_id, self.__result,
                                                    "Направильно вказано діапазон кодів(умову не зараховано)")

            name = name_in.get()
            self.__result = search.search_text_having_none("name", name, self.__result)

            surname = surname_in.get()
            self.__result = search.search_text_having_none("surname", surname, self.__result)

            salary_from = from_salary.get()
            salary_to = to_salary.get()
            self.__result = search.search_diapazone("salary", salary_from, salary_to, self.__result,
                                                    "Направильно вказано діапазон цін(умову не зараховано)")

            phone = phone_in.get()
            self.__result = search.search_text_having_none("phoneNumber", phone, self.__result)

            self.clear_table()
            for index, row in self.__result.iterrows():
                values = tuple(row.values)
                self._Window__table.insert("", tk.END, values=values)

        submit = ctk.CTkButton(search_win, text="Знайти", command=search_g)
        submit.grid(stick="ew", row=11, columnspan=2, pady=20, padx=40)

        search_win.mainloop()

    def create(self):
        create_win = ctk.CTk()
        create_win.title("Створення")

        top = ctk.CTkLabel(create_win, text="Створення", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        name_label = ctk.CTkLabel(create_win, text="Ім'я продавця", font=("Times New Roman", 15))
        name_label.grid(stick="ew")
        name_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        name_in.grid(stick="ew", padx=10)

        surname_label = ctk.CTkLabel(create_win, text="Прізвище продавця", font=("Times New Roman", 15))
        surname_label.grid(stick="ew")
        surname_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        surname_in.grid(stick="ew", padx=10)

        salary_label = ctk.CTkLabel(create_win, text="Зарплата", font=("Times New Roman", 15))
        salary_label.grid(stick="ew")
        salary_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        salary_in.grid(stick="ew", padx=10)

        phone_label = ctk.CTkLabel(create_win, text="Номер телефону", font=("Times New Roman", 15))
        phone_label.grid(stick="ew")
        phone_in = ctk.CTkEntry(create_win, font=("Times new Roman", 15))
        phone_in.grid(stick="ew", padx=10)

        def add():
            cus_id = random.randint(30, 100000000)
            name = name_in.get()
            surname = surname_in.get()
            salary = salary_in.get()
            phone = phone_in.get()

            list_args = [cus_id]

            if not name == "":
                list_args.append(str(name))
            else:
                messagebox.showwarning("Warning", "Не вказано імені")
                return

            if not surname == "":
                list_args.append(str(surname))
            else:
                messagebox.showwarning("Warning", "Не вказано прізвища")
                return

            if not salary == "":
                try:
                    salary = int(salary)
                    list_args.append(salary)
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно вказано зарплату")
                    return
            else:
                messagebox.showwarning("Warning", "Не вказано зарплату")
                return

            if not phone == "":
                try:
                    int(phone)
                    list_args.append(str(phone))
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно вказано номер телефону")
                    return
            else:
                messagebox.showwarning("Warning", "Не вказано номеру телефону")
                return

            list_args = tuple(list_args)

            self._Window__cursor.execute("INSERT INTO sellers VALUES " + str(list_args) + ";")
            admin.commit()

        submit = ctk.CTkButton(create_win, text="Створити", command=add)
        submit.grid(stick="ew", pady=20, padx=40)

        create_win.mainloop()

    def delete_selected_item(self, **kwargs):
        try:
            super().delete_selected_item("sellerID", "sellers")
        except Exception as e:
            if str(e) == "1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`store`.`orders`, CONSTRAINT `fk_seller` FOREIGN KEY (`sellerID`) REFERENCES `sellers` (`sellerID`))":
                messagebox.showwarning("showwarning", "Даний продавець застосований у іншій таблиці")

    def edit(self):
        p_id = self._Window__edit_en.get()
        all_id = pd.read_sql("SELECT sellerID FROM sellers", con=admin)
        all_id = all_id["sellerID"].tolist()
        try:
            p_id = int(p_id)
        except ValueError:
            messagebox.showwarning("warning", "Неправильно введено код продавця")
            return

        if p_id not in all_id:
            messagebox.showwarning("Warning", "Немає такого продавця")
            return

        edit_win = ctk.CTk()
        edit_win.title("Редагування")

        top = ctk.CTkLabel(edit_win, text="Редагування", font=("Times New Roman", 28))
        top.grid(stick="ew", pady=10)

        name_label = ctk.CTkLabel(edit_win, text="Ім'я продавця", font=("Times New Roman", 15))
        name_label.grid(stick="ew")
        name_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        name_in.grid(stick="ew", padx=10)

        surname_label = ctk.CTkLabel(edit_win, text="Прізвище продавця", font=("Times New Roman", 15))
        surname_label.grid(stick="ew")
        surname_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        surname_in.grid(stick="ew", padx=10)

        salary_label = ctk.CTkLabel(edit_win, text="Зарплата", font=("Times New Roman", 15))
        salary_label.grid(stick="ew")
        salary_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        salary_in.grid(stick="ew", padx=10)

        phone_label = ctk.CTkLabel(edit_win, text="Номер телефону", font=("Times New Roman", 15))
        phone_label.grid(stick="ew")
        phone_in = ctk.CTkEntry(edit_win, font=("Times new Roman", 15))
        phone_in.grid(stick="ew", padx=10)

        def edit_q():

            name = name_in.get()
            surname = surname_in.get()
            salary = salary_in.get()
            phone = phone_in.get()

            if not name == "":
                self._Window__cursor.execute(
                    "UPDATE sellers SET name = '" + str(name) + "' WHERE sellerID = " + str(p_id) + ";")
                admin.commit()

            if not surname == "":
                self._Window__cursor.execute(
                    "UPDATE sellers SET surname = '" + str(surname) + "' WHERE sellerID = " + str(p_id) + ";")
                admin.commit()

            if not salary == "":
                try:
                    salary = int(salary)
                    self._Window__cursor.execute(
                        "UPDATE sellers SET Salary = " + str(salary) + " WHERE sellerID = " + str(p_id) + ";")
                    admin.commit()
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно введено зарплату")

            if not phone == "":
                try:
                    phone = int(phone)
                    self._Window__cursor.execute(
                        "UPDATE sellers SET phoneNumber = '" + str(phone) + "' WHERE sellerID = " + str(p_id) + ";")
                    admin.commit()
                except ValueError:
                    messagebox.showwarning("Warning", "Неправильно введено номер")

        submit = ctk.CTkButton(edit_win, text="Змінити", command=edit_q)
        submit.grid(stick="ew", pady=20, padx=40)

        edit_win.mainloop()

    def sort(self):
        type_s = self._Window__type_of_sort.get()
        sort_type = None
        match type_s:
            case "Код продавця":
                sort_type = "sellerID"
            case "Ім'я":
                sort_type = "name"
            case "Прізвище":
                sort_type = "surname"
            case "Зарплата":
                sort_type = "salary"
        if sort_type:
            self.__result = pd.read_sql("""
                                    SELECT *
                                    FROM sellers 
                                    ORDER BY """ + sort_type + ";", con=admin)

            self.clear_table()
            for index, row in self.__result.iterrows():
                values = tuple(row.values)
                self._Window__table.insert("", tk.END, values=values)

    def to_doc(self, **kwargs):
        super().to_doc(self.__result)


# ---------------------------------------------------------------------------------------------------------------
class AdminWindow:
    def __init__(self):
        self.__win = ctk.CTk()
        self.__win.geometry("450x350+600+220")
        self.__win.title("Магазин гаджетів")
        self.__win.resizable(False, False)
        self.__win.protocol("WM_DELETE_WINDOW", self.on_closing)

        top_title = ctk.CTkLabel(self.__win,
                                 text="Магазин гаджетів",
                                 font=("Times new Roman", 24))
        top_title.pack(side=ctk.TOP, fill=ctk.X, pady=10)

        self.__buttons = ctk.CTkFrame(self.__win)
        self.__buttons.pack(padx=10)

        self.__products = ctk.CTkButton(self.__buttons, text="Робота з товарами", command=self.products)
        self.__products.grid(pady=10, stick='ew', row=0, column=0)

        self.__orders = ctk.CTkButton(self.__buttons, text="Робота з замовленнями", command=self.orders)
        self.__orders.grid(pady=10, stick='ew', row=1, column=0)

        self.__vendors = ctk.CTkButton(self.__buttons, text="Робота з постачальниками", command=self.vendors)
        self.__vendors.grid(pady=10, stick='ew', row=2, column=0)

        self.__customers = ctk.CTkButton(self.__buttons, text="Робота з покупцями", command=self.customers)
        self.__customers.grid(pady=10, stick='ew', row=3, column=0)

        self.__sellers = ctk.CTkButton(self.__buttons, text="Робота з продавцями", command=self.sellers)
        self.__sellers.grid(pady=10, stick="ew", row=4, column=0)
        self.__win_p = ProductsWin()
        self.__win_o = OrdersWin()
        self.__win_c = CustomersWin()
        self.__win_v = VendorsWin()
        self.__win_s = SellersWin()

    def orders(self):
        self.__win_o.run()

    def products(self):
        self.__win_p.run()

    def vendors(self):
        self.__win_v.run()

    def sellers(self):
        self.__win_s.run()

    def customers(self):
        self.__win_c.run()

    def run(self):
        self.__win.mainloop()

    def on_closing(self):
        self.__win_p.on_closing()
        self.__win_o.on_closing()
        self.__win_c.on_closing()
        self.__win_s.on_closing()
        self.__win_v.on_closing()
        self.__win.destroy()


admin_win = AdminWindow()
admin_win.run()
