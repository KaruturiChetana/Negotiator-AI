from uagents import Agent

from protocols import negotiator_protocol

agent = Agent()

agent.include(negotiator_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
