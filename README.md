# Beneficient Risk Developer Coding Test #
This repo contains a coding test for potential risk developers.
We do not expect you to know [Dash](https://dash.plotly.com/) but expect you to be able to
quickly learn whatever you need in order to finish the project through online resources yourself.
Please feel free to add any comments in the code. After you are done, please zip the project folder and email the zip file
to your recruiter who will send to us.

### How do I get set up? ###
1. Create a clean python environment with whatever environment manager you prefer (virtualenv, conda, etc.)
2. Activate environment created in step 1
3. Execute ``pip install dash pandas`` to install dash and pandas
4. Launch app by running ``python app.py``

### Tasks for Candidate to Perform ###
The following tasks should be completed by the candidate in their preferred order:

* Complete the ``Observation.delete_matching`` method in cpi.py which contains detailed instructions.
* When the "Delete Matching Observations" button is clicked, the ``Observation.delete_matching`` method is called and
  the database table, front-end table, and front-end graph are updated accordingly.
* When the "Graph Type" drop-down is set to "Item Price Over Time", multiple observations for the
  same item that have the same price causes the point size to scale proportionately to the number of matching
  observations
* Implement the "Average Item Price by City" graph type so that when it is selected, it changes the graph to a grouped
  bar graph where the height of a bar is the average price of an item in a city for the date in the "Date"
  field. The bars should be grouped together by item type and the color of each bar should correspond to the city that
  the average item price applies to. [Example of a grouped bar graph](https://chartio.com/assets/24e451/tutorials/charts/grouped-bar-charts/c1fde6017511bbef7ba9bb245a113c07f8ff32173a7c0d742a4e1eac1930a3c5/grouped-bar-example-1.png)

### Bonus Tasks ###
* Please feel free to add any enhancements to the code that will make it production-level quality including:
  - Improving the layout, look, and feel of the app
  - Add data validations which make sense for the business logic
  - Improve the data formatting for cleanliness and to be inline with American business conventions
  - You are encouraged to refactor existing code if doing so will improve readability, extendability, performance, etc.
  - Add tests to verify the behavior and impact of code changes
* Any enhancements that you have added should be documented in the README.md section below called ``Enhancements``

### Grading Criteria ###
* Completion of the tasks specified and the bonus tasks
* Maintainability and readability of code written
* Thoughtful comments and descriptive variable names
* Code execution performance (there should be no noticeable delay to the user when changing graphs or deleting points)

### Who do I talk to? ###
* recruiting@beneficient.com

### Enhancements ###
* Added dash bootstrap components to style the various inputs fields and buttons and also place restrictions on arguments accepted. This is to ensure data integrity.
* Changed the typography used in the app to make it more visible.
* Added .pre-commit-config.yaml file to format with black on commit
* Made Price and Number of Mactching Obesevations a requirened numberic input
* Sorted dash table to show most recent records at the top
* Formatted dash table to paginate records increase readability
* Addded data validation to not add observations when required field id not submitted.
* Connected State and City dropdowns to allow the user access to cities that match selected state
* Added style.css to customize UI and improve UX
* Added Test to test wirte method observation
