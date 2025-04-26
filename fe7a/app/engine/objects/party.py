from app.engine.objects.item import ItemObject
from app.utilities.data import Prefab

from app.engine.game_state import game
from typing import List, Optional
from app.utilities.typing import NID

class PartyObject(Prefab):
    def __init__(self, nid: NID, name: str, leader_nid: NID, party_prep_manage_sort_order: Optional[List[NID]]=None,
                 money: int = 0, convoy: Optional[List[int]] = None, bexp: int = 0):
        """Representation of a party of units. Unless you have a multi-party game, game.party will generally return
        the information you need for your party of units.

        `my_money_value = game.party.money`
        
        Distinguishes units who belong in a single party from one another and separates their convoy, money, and bexp.
        
        Args:
            nid (NID): Unique ID for the party
            name (str): Name of the party
            leader_nid (NID): Unit NID of the leader of the party
            money (int): How much money the party has
            convoy (Optional[List[int]], optional): List of items the party's convoy contains
            bexp (int, optional): How much bonus experience the party has access to
        """
        self.nid = nid
        self.name = name
        self.leader_nid = leader_nid
        self.party_prep_manage_sort_order = party_prep_manage_sort_order or []  # Unit nids (The order is used for the prep and manage screen and NOTHING ELSE)
        self.money = money
        self.convoy: List[ItemObject] = []
        if convoy:
            # Actually the item, not just a uid reference
            items = [game.get_item(item_uid) for item_uid in convoy]
            self.convoy = [i for i in items if i]
        self.bexp: int = bexp

    @property
    def items(self):
        return self.convoy

    def save(self):
        return {'nid': self.nid,
                'name': self.name,
                'leader_nid': self.leader_nid,
                'party_prep_manage_sort_order': self.party_prep_manage_sort_order,
                'money': self.money,
                'convoy': [item.uid for item in self.convoy],
                'bexp': self.bexp}

    @classmethod
    def restore(cls, s_dict):
        party = cls(s_dict['nid'], s_dict.get('name', s_dict['nid']), s_dict['leader_nid'],
                    s_dict.get('party_prep_manage_sort_order', []), s_dict.get('money', 0), s_dict.get('convoy', []),
                    s_dict.get('bexp', 0))
        return party
