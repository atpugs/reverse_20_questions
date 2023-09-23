# Reversing the Twenty Questions Game

Twenty questions is a widely popular verbal game. In recent years, many computerized versions of this game have been developed in which a user thinks of an entity and a computer attempts to guess this entity by asking a series of boolean-type (yes/no) questions. In this research, we aim to reverse this game by making the computer choose an entity at random. The human aims to guess this entity by quizzing the computer with natural language queries which the computer will then attempt to parse using a boolean question answering model. The game ends when the human is successfully able to guess the entity of the computer’s choice.

## Entity Formulation and Pronoun Resolution
Our proposed model starts by selecting a random Wikipedia page of a named entity. This entity acts as our model’s main entity - the guess. These random Wikipedia pages can be extracted by passing SPARQL queries to Wikidata [7]. The model then accepts natural language queries from a user. As the first step, each of these queries undergoes a basic pronoun resolution wherein a pronoun gets replaced with the model’s main entity. For example, the model is likely to predict better results if we formulate the query in the following manner -

Is it an animated character? → Is Mickey Mouse an animated character?

This step ensures that our model does not easily get confused when it sees another entity with a similar context.

To obtain a relevant passage from the entity’s Wikipedia text, we require a passage retrieval phase. Here, relevance can be defined as a passage from the main entity’s text-body which unambiguously answers a boolean-type query. For example -

Is Mickey Mouse a comic book character?

“Beginning in 1930, Mickey has also been featured extensively in comic strips and comic books. The Mickey Mouse comic strip, drawn primarily by Floyd Gottfredson, ran for 45 years. Mickey has also appeared in comic books such as Mickey Mouse, Disney Italy’s Topolino and MM – Mickey Mouse Mystery Magazine, and Wizards of Mickey.” <br>
- From the Wikipedia page of Mickey Mouse (paragraph 3)

To guess the boolean-type response, we propose a transformer-based model which takes as its input a query and N2 relevant paragraphs. We plan on experimenting with a BERT model pre-trained on entailment tasks and fine-tuned using the BoolQ dataset. While playing games with Akinator, we observed that a certain class of questions can be answered using knowledge repositories such as Wikidata and DBpedia. These questions involve highly distinguishing characteristics of the entity such as its gender, species, hypernyms, and significant others.

## Experiments
In our experiments, we employed the Akinator API to test our model's performance, using akinator.py to simulate the original Akinator's guessing mechanism. We initially implemented a baseline model which answered the Akinator’s questions randomly. However, this approach often led to Akinator guessing non-specific entities, indicating random guessing on our part. To improve upon this, we developed a more sophisticated model, incorporating the Okapi-BM25/SBERT pipeline. We further constrained our domain to English animal names to make the problem more tractable. Challenges arose in discerning between actual animal references and cultural mentions, which we mitigated by integrating data from Simple Wikipedia alongside the standard Wikipedia. Lastly, we experimented with different neural architectures, including DistilBERT and RoBeRTa-base, fine-tuning them on the BoolQ dataset. The RoBeRTa-base model showed promising results with a development-set accuracy of 80.7%, significantly outperforming our initial implementations.

To enhance our model's performance, we implemented a negative sampling approach, which aids in determining the accuracy of answers obtained from BM25 and cosine similarity, especially when specific characteristics about an animal are absent in its Wikipedia article. If an answer doesn't match the expected response for a correct animal, we select one entity from a broad taxonomy of animals, treating these as negative samples. By comparing scores between these negative samples and our main animal, we can discern the reliability of our answer. Additionally, we trained a model to enhance the yes/no response by considering text score statistics of the negative samples. Our experiments also revealed the Akinator's sensitivity to answers and its volatile guessing pattern. We introduced a technique to detect misleading answers using negative sampling results and rectify them using positive samples. This strategy identifies and fixes detours, ensuring the Akinator is guided towards the correct animal more consistently.

<p align="center">
  <img src="https://github.com/atpugs/reverse_20_questions/assets/31329834/a3d14830-4017-4889-826d-536a98bd1efb">
  Example of negative sampling
</p>

<p align="center">
  <img src="https://github.com/atpugs/reverse_20_questions/assets/31329834/9b7a6b77-887f-49a7-a998-5ba2c8bbe75b">
  Example game for animal cheetah
</p>


## Model Evaluation
To evaluate our model, we utilized metrics such as accuracy, recall, precision, and F1 score based on the BoolQ test set. Additionally, benchmark datasets like GLUE and SuperGLUE were used for submodel evaluations. Upon hand-annotating 250 questions, we found an accuracy of 78.69% with our pipeline's outputs. We also devised an approximate answering technique that assessed the correct yes/no answer based on the Akinator's response. This resulted in a 62.88% accuracy rate over 264 automatically generated questions.

To gain deeper insights, we introduced metrics like detour recovery time and best guess probability. The former measures how quickly the Akinator returns to the correct animal after being misled, averaging about 8 questions. The latter observes the peak probability of the correct animal being guessed during a game, averaging at 25.91%. For future evaluations, we suggest implementing a convergence rate metric, which will assess the growth rate of the Akinator's confidence in its guesses over time.

## Further reading
For more information, please refer our project paper: https://arxiv.org/pdf/2301.08718.pdf
