# DSCI-532_2024_13_Juno
[![](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Members:
- Riya Shaju
- Gretel Tan
- Karan Khubdikar
- Scout McKee

# Juno

This project scrutinizes the gender disparity in top-level leadership roles within Canadian corporations across multiple sectors. Leveraging gender-disaggregated data, we aim to reveal the potential influence of gender balance in decision-making roles on more effective and inclusive policies.

Ancient Romans worshipped Juno as the queen of the gods, the female counterpart to the chief of the gods, Jupiter. Since our app looks at the gender makeup of the top-level management in companies across Canada, we felt that Juno, as the CEO/COO equivalent of the Roman pantheon, would be a good representation of the female leaders we are highlighting in our data set. Furthermore, Juno's close association with women and her status as the protector of women resonates with our more aspirational goal, which is to uncover potential areas for improving inclusivity and gender equality in Canadian corporations. As a champion of women, and a prominent female leader herself, we feel that Juno is a good symbol of what we strive to achieve with this app. We have thus named our app after her.

# Motivation

## The Problem: 
Despite progress in workplace diversity initiatives, gender disparity remains a pervasive issue at the highest levels of leadership, with men disproportionately represented compared to women. 

## The Solution:
Our dashboard app aims to shed light on this disparity by providing visual insights into the gender composition of top-level leadership, highlighting the need for continued efforts to achieve gender equality and foster inclusive workplaces. The dashboard allows the user to deep-dive into several aspects such as Types of Corporations, Industries, or Provinces, and also look into specific years.

# How to use this app

We have deployed our app on Render, feel free to access it [here](https://dsci-532-2024-13-juno-aa9o.onrender.com/) and try it out for yourself! It has a simple click-based GUI, where you can explore different subsets of the data based on province, industry, and time period. You can use this app to explore different summary statistics and graphs that highlight important insights in helping us understand trends in the gender makeup of top positions in Canadian corporations.

# Demo of the app

Here, you can view a GIF demonstrating how our app works:

![GIF](https://raw.githubusercontent.com/UBC-MDS/DSCI-532_2024_13_Juno/blob/main/img/demo.gif) 

# Running the dashboard locally
1. Clone the repository
```
git clone https://github.com/UBC-MDS/DSCI-532_2024_13_Juno.git
cd DSCI-532_2024_13_Juno
```
2. Create a virtual environment and activate it
```
conda env create -f environment.yml
conda activate Juno_env
```
3. Set the `debug=True` in the `app.py` for the development
```
if __name__ == "__main__":
    app.run(debug=True)
```
4. Render the dashboard locally
**Note:** You might have to update the data.py file and update the path (remove `../` from the file path)
```
python src/app.py
```
5. Click on the link(`http://127.0.0.1:8052/`) or copypaste it into a browser to view the dashboard


# Contribute to our repo!

We would love for you to contribute to our app. Here's how to get started!

1.  Fork the `DSCI-532_2024_13_Juno` repo on GitHub.

2.  Clone your fork locally:

    ```         
    https://github.com/UBC-MDS/DSCI-532_2024_13_Juno.git
    ```

3.  Create a branch for local development:

    ```         
    git checkout -b name-of-your-bugfix-or-feature
    ```

    Now you can make your changes locally.

4.  When you're done making changes, commit your changes and push your branch to GitHub:

    ```         
    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature
    ```

5.  Submit a pull request through the GitHub website.

# Get in touch

Stuck in a bind? Have an idea for a useful feature, but have no idea how to implement it? We got you! Please feel free to raise an issue to let us know! Let us work together toward uncovering gender biases and empowering women :)
