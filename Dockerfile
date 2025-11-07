FROM python
WORKDIR /tests_project/
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV ENV=dev
CMD python3 -m pytest -s --alluredir=test_results/ /test_project/tests/