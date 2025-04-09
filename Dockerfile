# Step 1: Use Miniconda as the base image
FROM continuumio/miniconda3:latest

# Step 2: Set working directory inside the container
WORKDIR /app

# Step 3: Copy the environment.yaml to the container
COPY tensorflow-flask_final.yaml /app/

# Step 4: Create the conda environment based on your .yaml file
RUN conda env create -f tensorflow-flask_final.yaml

# Step 5: Set the environment to use the newly created conda environment
# This will activate the environment when the container runs
RUN echo "conda activate base" >> ~/.bashrc

# Step 6: Install gunicorn to serve the Flask app
RUN conda activate base && pip install gunicorn

# Step 7: Copy the rest of your application files to the container
COPY . /app/

# Step 8: Expose port 5000 (default for Flask)
EXPOSE 5000

# Step 9: Command to run the Flask app using Gunicorn
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:5000"]

